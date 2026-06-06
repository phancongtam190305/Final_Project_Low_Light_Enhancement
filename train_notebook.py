import marimo

__generated_with = "0.23.8"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    import torch.optim as optim
    from torch.utils.tensorboard import SummaryWriter
    import os
    import time
    import matplotlib.pyplot as plt
    import numpy as np

    from models import Zero_DCE, Zero_DCE_PP, ZDCE_ResBlock_Small, ZDCE_DenseBlock_Small
    from utils import LOLDataset, VGGPerceptualLoss, calculate_metrics_numpy

    return (
        DataLoader,
        LOLDataset,
        SummaryWriter,
        VGGPerceptualLoss,
        ZDCE_DenseBlock_Small,
        ZDCE_ResBlock_Small,
        Zero_DCE,
        Zero_DCE_PP,
        calculate_metrics_numpy,
        mo,
        nn,
        np,
        optim,
        os,
        plt,
        time,
        torch,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # ⚡ Low-Light Image Enhancement - Training Dashboard
    Chào mừng bạn đến với dashboard huấn luyện các mô hình Low-Light Enhancement. Dashboard này được xây dựng bằng **Marimo** cho phép bạn cấu hình trực quan và theo dõi quá trình huấn luyện thời gian thực.
    """)
    return


@app.cell
def _(mo, torch):
    # Cấu hình giao diện chọn tham số
    model_selector = mo.ui.dropdown(
        options={
            "Zero-DCE (Baseline)": "Zero_DCE",
            "Zero-DCE++ (Lightweight)": "Zero_DCE_PP",
            "ZDCE+-ResBlock-Small (Biến thể ResBlock)": "ZDCE_ResBlock_Small",
            "ZDCE+-DenseBlock-Small (Biến thể DenseBlock)": "ZDCE_DenseBlock_Small",
        },
        value="Zero_DCE",
        label="Chọn mô hình huấn luyện:",
    )

    data_dir_input = mo.ui.text(
        value="./data",
        placeholder="Đường dẫn đến thư mục LOL-v1",
        label="Đường dẫn dữ liệu (data_dir):",
    )

    epochs_slider = mo.ui.slider(
        start=5,
        stop=100,
        step=5,
        value=50,
        label="Số Epochs:",
    )

    batch_size_selector = mo.ui.dropdown(
        options=["4", "8", "16", "32"],
        value="16",
        label="Batch Size:",
    )

    lr_input = mo.ui.text(
        value="1e-4",
        label="Learning Rate:",
    )

    weight_decay_input = mo.ui.text(
        value="1e-4",
        label="Weight Decay:",
    )

    device_selector = mo.ui.dropdown(
        options=["cuda", "cpu"],
        value="cuda" if torch.cuda.is_available() else "cpu",
        label="Thiết bị (Device):",
    )

    # Nút trigger huấn luyện
    start_train_btn = mo.ui.button(
        label="🚀 Bắt đầu Huấn luyện",
        tooltip="Click để kích hoạt vòng lặp train"
    )

    mo.md(
        f"""
        ### ⚙️ Cấu Hình Huấn Luyện
        Thiết lập các siêu tham số huấn luyện trước khi bắt đầu:

        *   {model_selector}
        *   {data_dir_input}
        *   {device_selector}
        *   {epochs_slider}
        *   {batch_size_selector}
        *   {lr_input} | {weight_decay_input}

        {start_train_btn}
        """
    )
    return (
        batch_size_selector,
        data_dir_input,
        device_selector,
        epochs_slider,
        lr_input,
        model_selector,
        start_train_btn,
        weight_decay_input,
    )


@app.cell
def _(
    DataLoader,
    LOLDataset,
    SummaryWriter,
    VGGPerceptualLoss,
    ZDCE_DenseBlock_Small,
    ZDCE_ResBlock_Small,
    Zero_DCE,
    Zero_DCE_PP,
    batch_size_selector,
    calculate_metrics_numpy,
    data_dir_input,
    device_selector,
    epochs_slider,
    lr_input,
    mo,
    model_selector,
    nn,
    np,
    optim,
    os,
    plt,
    start_train_btn,
    time,
    torch,
    weight_decay_input,
):
    import io

    chart = None
    latest_val_sample_img = None
    error_msg = None

    if start_train_btn.clicked:
        model_name = model_selector.value
        data_dir = data_dir_input.value
        epochs = int(epochs_slider.value)
        batch_size = int(batch_size_selector.value)
        lr = float(lr_input.value)
        weight_decay = float(weight_decay_input.value)
        device = torch.device(device_selector.value)
        pin_memory = device.type == 'cuda'

        # 1. Khởi tạo dataset & dataloader
        try:
            train_dataset = LOLDataset(data_dir, split='train')
            val_dataset = LOLDataset(data_dir, split='val')
        except Exception as e:
            error_msg = mo.md(f"❌ **Lỗi tải dữ liệu:** {e}. Hãy đảm bảo bạn đã đặt dataset LOL-v1 đúng cấu trúc `./data/our485` và `./data/eval15`.")
            train_dataset = None

        if train_dataset is not None:
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=pin_memory)
            val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False, num_workers=0, pin_memory=pin_memory)

            # 2. Khởi tạo model
            model_class_map = {
                "Zero_DCE": Zero_DCE,
                "Zero_DCE_PP": Zero_DCE_PP,
                "ZDCE_ResBlock_Small": ZDCE_ResBlock_Small,
                "ZDCE_DenseBlock_Small": ZDCE_DenseBlock_Small
            }
            model = model_class_map[model_name]().to(device)

            # 3. Định nghĩa optimizer, scheduler và losses
            optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
            scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

            l1_loss_fn = nn.L1Loss()
            perceptual_loss_fn = VGGPerceptualLoss().to(device)

            use_amp = (device.type == 'cuda')
            scaler = torch.amp.GradScaler(device.type, enabled=use_amp)

            os.makedirs("./checkpoints", exist_ok=True)
            os.makedirs("./runs", exist_ok=True)

            writer = SummaryWriter(log_dir=f"./runs/{model_name}_{time.strftime('%m%d_%H%M%S')}")

            train_losses = []
            val_psnrs = []
            val_ssims = []

            best_psnr = -1.0

            # Lấy sẵn 1 ảnh mẫu từ tập validation để theo dõi suốt quá trình train
            sample_low, sample_high = val_dataset[0]  # lấy ảnh đầu tiên
            sample_low_tensor = sample_low.unsqueeze(0).to(device)

            # Khởi tạo thanh tiến trình Marimo
            with mo.status.progress(title="Đang Huấn luyện...", max=epochs) as progress:
                for epoch in range(epochs):
                    model.train()
                    epoch_loss = 0.0

                    for low_img, high_img in train_loader:
                        low_img = low_img.to(device)
                        high_img = high_img.to(device)

                        optimizer.zero_grad()

                        with torch.amp.autocast(device_type=device.type, enabled=use_amp):
                            enhanced_img = model(low_img)
                            loss_l1 = l1_loss_fn(enhanced_img, high_img)
                            loss_vgg = perceptual_loss_fn(enhanced_img, high_img)
                            loss = loss_l1 + 0.01 * loss_vgg

                        scaler.scale(loss).backward()
                        scaler.unscale_(optimizer)
                        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                        scaler.step(optimizer)
                        scaler.update()

                        epoch_loss += loss.item() * low_img.size(0)

                    epoch_loss /= len(train_dataset)
                    train_losses.append(epoch_loss)
                    scheduler.step()

                    writer.add_scalar("Loss/Train", epoch_loss, epoch + 1)

                    # Đánh giá trên tập validation
                    model.eval()
                    epoch_psnrs = []
                    epoch_ssims = []

                    with torch.no_grad():
                        for low_img_val, high_img_val in val_loader:
                            low_img_val = low_img_val.to(device)
                            high_img_val = high_img_val.to(device)

                            enhanced_val = model(low_img_val)
                            psnr, ssim = calculate_metrics_numpy(enhanced_val, high_img_val)
                            epoch_psnrs.append(psnr)
                            epoch_ssims.append(ssim)

                    mean_psnr = np.mean(epoch_psnrs)
                    mean_ssim = np.mean(epoch_ssims)
                    val_psnrs.append(mean_psnr)
                    val_ssims.append(mean_ssim)

                    writer.add_scalar("Metrics/Val_PSNR", mean_psnr, epoch + 1)
                    writer.add_scalar("Metrics/Val_SSIM", mean_ssim, epoch + 1)

                    # Sinh ảnh so sánh trực quan thời gian thực từ ảnh mẫu
                    with torch.no_grad():
                        sample_enhanced = model(sample_low_tensor)

                    # Convert tensor -> numpy
                    low_np = sample_low.cpu().numpy().transpose(1, 2, 0)
                    high_np = sample_high.cpu().numpy().transpose(1, 2, 0)
                    enhanced_np = sample_enhanced[0].cpu().numpy().transpose(1, 2, 0)

                    low_np = np.clip(low_np, 0, 1)
                    high_np = np.clip(high_np, 0, 1)
                    enhanced_np = np.clip(enhanced_np, 0, 1)

                    # Tạo plot
                    fig_sample, axes = plt.subplots(1, 3, figsize=(10, 4))
                    axes[0].imshow(low_np)
                    axes[0].set_title("Input (Low Light)")
                    axes[0].axis('off')

                    axes[1].imshow(enhanced_np)
                    axes[1].set_title(f"Enhanced (Epoch {epoch+1})")
                    axes[1].axis('off')

                    axes[2].imshow(high_np)
                    axes[2].set_title("Ground Truth")
                    axes[2].axis('off')

                    plt.tight_layout()

                    # Lưu plot vào bytes buffer để truyền vào mo.image
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
                    buf.seek(0)
                    latest_val_sample_img = buf.read()
                    plt.close(fig_sample)

                    if mean_psnr > best_psnr:
                        best_psnr = mean_psnr
                        torch.save(
                            {
                                'epoch': epoch + 1,
                                'model_state_dict': model.state_dict(),
                                'optimizer_state_dict': optimizer.state_dict(),
                                'psnr': mean_psnr,
                                'ssim': mean_ssim,
                            },
                            f"./checkpoints/best_{model_name}.pth"
                        )

                    progress.update(
                        value=epoch + 1,
                        subtitle=f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss:.4f} | Val PSNR: {mean_psnr:.2f}dB | Best PSNR: {best_psnr:.2f}dB"
                    )

            writer.close()

            # Vẽ đồ thị kết quả cuối cùng
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            axes[0].plot(range(1, len(train_losses) + 1), train_losses, label="Train Loss", color="royalblue", lw=2)
            axes[0].set_title("Training Loss History")
            axes[0].set_xlabel("Epoch")
            axes[0].set_ylabel("Loss")
            axes[0].grid(True, linestyle="--", alpha=0.6)
            axes[0].legend()

            axes[1].plot(range(1, len(val_psnrs) + 1), val_psnrs, label="Val PSNR (dB)", color="crimson", lw=2)
            axes[1].set_title("Validation PSNR History")
            axes[1].set_xlabel("Epoch")
            axes[1].set_ylabel("PSNR (dB)")
            axes[1].grid(True, linestyle="--", alpha=0.6)
            axes[1].legend()

            plt.tight_layout()
            chart = mo.as_html(fig)
            plt.close()
    return chart, error_msg, latest_val_sample_img


@app.cell
def _(chart, error_msg, latest_val_sample_img, mo, start_train_btn):
    # Hiển thị kết quả & Ảnh so sánh mẫu hoặc thông báo lỗi
    if not start_train_btn.clicked:
        output = mo.md("👉 *Nhấn nút **Bắt đầu Huấn luyện** ở trên để khởi chạy quá trình.*")
    elif error_msg is not None:
        output = error_msg
    elif latest_val_sample_img is not None:
        sample_display = mo.md(
            f"""
            ### 🖼️ Ảnh Tăng Sáng Thực Tế (Epoch Cuối Cùng)
            Dưới đây là kết quả tăng sáng thực tế trên một ảnh mẫu của tập validation:
            """
        )
        sample_img_el = mo.image(src=latest_val_sample_img)

        output = mo.vstack([
            sample_display,
            sample_img_el,
            mo.md(
                f"""
                ---
                ### 📈 Đồ Thị Quá Trình Huấn Luyện (Loss & PSNR)
                {chart}
                """
            )
        ])
    else:
        output = mo.md("⏳ *Đang chuẩn bị quá trình huấn luyện...*")
    return (output,)


@app.cell
def _(output):
    output
    return


if __name__ == "__main__":
    app.run()
