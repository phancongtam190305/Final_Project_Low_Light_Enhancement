# Khảo Sát Tập Dữ Liệu Nhánh 1: Paired Enhancement RGB

Tài liệu này thực hiện khảo sát chi tiết và hệ thống hóa thông tin khoa học của các tập dữ liệu ảnh cặp (paired datasets) cốt lõi trong nghiên cứu Tăng cường Ảnh Thiếu Sáng RGB (RGB Low-Light Image Enhancement - LLIE). Các tập dữ liệu được khảo sát bao gồm: **LOL (LOw-Light)**, **LOL-v2 (Real & Synthetic)** và **SICE (Single Image Contrast Enhancer)**.

---

## 1. Bảng 1: Thông Tin Cơ Bản (Basic Information)

Bảng này cung cấp các thông tin nền tảng về nguồn gốc lịch sử, quy mô dữ liệu, định dạng vật lý và tính pháp lý của từng tập dữ liệu.

| Tiêu Chí | LOL (v1) | LOL-v2 (Real) | LOL-v2 (Synthetic) | SICE (Single Image Contrast Enhancer) |
| :--- | :--- | :--- | :--- | :--- |
| **Năm công bố** | 2018 | 2021 | 2021 | 2018 |
| **Hội nghị / Tạp chí** | BMVC 2018 | CVPR 2021 | CVPR 2021 | IEEE TIP 2018 |
| **Nhóm tác giả / Đơn vị** | Chen Wei, Wenjing Wang, Wenhan Yang, Jiaying Liu <br>*(Peking University)* | Wei Chen, Wenjing Wang, Wenhan Yang, Jiaying Liu <br>*(Peking University)* | Wei Chen, Wenjing Wang, Wenhan Yang, Jiaying Liu <br>*(Peking University)* | Jianrui Cai, Shuhang Gu, Lei Zhang <br>*(Hong Kong Polytechnic University)* |
| **Link download chính thức** | [LOL Dataset](https://cchen156.github.io/LOLdataset.html) | [LOL-v2 GitHub](https://github.com/flyywh/Awesome-Low-Light-Enhancement) | [LOL-v2 GitHub](https://github.com/flyywh/Awesome-Low-Light-Enhancement) | [SICE Repository](https://github.com/caojianrui/SICE) |
| **Tổng số lượng cặp ảnh** | 500 cặp ảnh (Low/Normal) | 789 cặp ảnh (Low/Normal) | 1,000 cặp ảnh (Low/Normal) | 589 chuỗi đa phơi sáng (Tổng cộng 4,413 ảnh) |
| **Phân chia Train / Test** | 485 Train / 15 Test | 689 Train / 100 Test | 900 Train / 100 Test | - Part 1: 360 chuỗi (3,022 ảnh)<br>- Part 2: 229 chuỗi (1,391 ảnh) |
| **Độ phân giải (Resolution)**| 400 × 600 pixels | 600 × 400 pixels | 384 × 284 pixels | Độ phân giải cao gốc (~3000 × 2000 trở lên) |
| **Định dạng dữ liệu** | sRGB (PNG, 8-bit) | sRGB (PNG, 8-bit) | sRGB (PNG, 8-bit) | sRGB (JPG, 8-bit) |
| **Bản quyền (License)** | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại |

---

## 2. Bảng 2: Đặc Tính Kỹ Thuật (Technical Characteristics)

Bảng này phân tích sâu các khía cạnh kỹ thuật liên quan đến phương pháp thu thập dữ liệu, cơ chế phơi sáng, kiểm soát nhiễu cảm biến, căn chỉnh pixel và độ đa dạng bối cảnh.

| Tiêu Chí Kỹ Thuật | LOL (v1) | LOL-v2 (Real) | LOL-v2 (Synthetic) | SICE (Single Image Contrast Enhancer) |
| :--- | :--- | :--- | :--- | :--- |
| **Thiết bị chụp / Quy trình tạo** | Chụp thực tế bằng máy DSLR chuyên nghiệp **Canon EOS 5D Mark II**. | Chụp thực tế bằng máy DSLR **Canon EOS 5D Mark II** và các thiết bị cầm tay. | Tổng hợp nhân tạo từ tập dữ liệu RAW chất lượng cao sử dụng Adobe DNG SDK. | Chụp thực tế trên chân máy cố định (tripod) bằng máy DSLR **Canon 5D Mark II** và **Nikon D800**. |
| **Cơ chế phơi sáng (Illumination)** | Thay đổi thời gian phơi sáng (exposure time) và độ nhạy sáng ISO. Ảnh tối có thời gian phơi sáng ngắn gấp 10-30 lần ảnh sáng. | Phơi sáng cực ngắn trong bối cảnh thực tế phức tạp để tạo độ tối sâu. | Mô phỏng quá trình suy giảm hạt ánh sáng và áp dụng mô hình toán học biến đổi tuyến tính. | Chụp phơi sáng từng bước (Bracketed Exposure) từ cực tối sang cực sáng (thường từ -4 EV đến +4 EV). |
| **Phương pháp tạo Ground Truth (GT)** | Ảnh phơi sáng chuẩn (Normal-light) được căn chỉnh trực tiếp làm GT. | Ảnh phơi sáng chuẩn được chọn lọc và căn chỉnh kỹ lưỡng làm GT. | Ảnh RAW gốc độ tương phản cao, đủ sáng được sử dụng làm GT lý tưởng. | Sử dụng 13 thuật toán Multi-Exposure Fusion (MEF) và Stack-based HDR hàng đầu để tổng hợp ra ảnh tham chiếu có dải động tối ưu nhất (High-Quality Reference). |
| **Căn chỉnh ảnh (Alignment)** | Sử dụng thuật toán so khớp đặc trưng **SIFT** để hiệu chỉnh dịch chuyển pixel do rung lắc nhỏ khi bấm máy. | Áp dụng SIFT kết hợp lọc thủ công nghiêm ngặt để loại bỏ hoàn toàn các cặp ảnh lệch. | Không cần căn chỉnh (Được tổng hợp từ một ảnh nguồn duy nhất nên khớp pixel tuyệt đối). | Ảnh chụp cố định trên chân máy chuyên dụng. Vẫn có thể gặp lỗi bóng mờ (ghosting) ở các vật thể động. |
| **Đặc tính Nhiễu (Noise & Artifacts)**| Nhiễu cảm biến thực tế (như nhiễu hạt màu - chroma noise và nhiễu độ sáng - luminance noise) xuất hiện rất nặng ở ảnh tối do khuếch đại ISO. | Mức độ nhiễu cực kỳ phức tạp và thực tế, phân bố không đều tại các vùng thiếu sáng. | Nhiễu Poisson-Gaussian nhân tạo được tiêm vào để mô phỏng chính xác hành vi vật lý của cảm biến ảnh ở photon thấp. | Nhiễu thấp ở các vùng phơi sáng dài, nhưng xuất hiện hiện tượng mất chi tiết do cháy sáng (over-exposure) hoặc cháy tối (under-exposure) ở các ảnh phơi sáng cực trị. |
| **Độ đa dạng bối cảnh** | Thấp. Chỉ bao gồm các cảnh tĩnh trong nhà (văn phòng, phòng khách, phòng thí nghiệm). Không chứa con người hay chuyển động. | Trung bình - Cao. Đã bổ sung nhiều bối cảnh ngoài trời, đường phố ban đêm và cấu trúc kiến trúc đa dạng. | Cao. Được tổng hợp từ kho ảnh phong phú đa chủ đề. | Cực kỳ cao. Bao gồm danh lam thắng cảnh, kiến trúc cổ kính, nội thất sang trọng, cảnh thiên nhiên ngoài trời với độ tương phản động cực lớn. |

---

## 3. Bảng 3: Protocol & Evaluation (Giao thức huấn luyện & Đánh giá)

Bảng này cung cấp các tiêu chuẩn đánh giá định lượng, phân chia dữ liệu huấn luyện/kiểm thử và ghi nhận hiệu năng nền tảng (baseline performance) của các mô hình đi trước.

| Tiêu Chí Đánh Giá | LOL (v1) | LOL-v2 (Real) | LOL-v2 (Synthetic) | SICE |
| :--- | :--- | :--- | :--- | :--- |
| **Phân chia huấn luyện mặc định** | 485 cặp ảnh để huấn luyện, 15 cặp ảnh để kiểm thử. Không có tập validation chính thức. | 689 cặp ảnh để huấn luyện, 100 cặp ảnh độc lập để kiểm thử. | 900 cặp ảnh để huấn luyện, 100 cặp ảnh độc lập để kiểm thử. | Part 1 (360 chuỗi đa phơi sáng) dùng huấn luyện. Part 2 (229 chuỗi) dùng đánh giá tổng quát hóa. |
| **Sự chồng chéo bối cảnh (Scene Overlap)** | Có sự chồng chéo nhất định giữa bối cảnh của tập huấn luyện và tập kiểm thử (cùng phòng nhưng góc chụp khác). | **Không chồng chéo**. Tập huấn luyện và tập kiểm thử được thiết kế chụp ở các bối cảnh địa lý hoàn toàn khác biệt. | **Không chồng chéo**. Đảm bảo kiểm tra khách quan năng lực tổng quát hóa của mô hình. | Thấp. Các địa điểm chụp và chuỗi bối cảnh độc lập hoàn toàn giữa Part 1 and Part 2. |
| **Metrics đánh giá chính** | Peak Signal-to-Noise Ratio (**PSNR**), Structural Similarity Index (**SSIM**), và Learned Perceptual Image Patch Similarity (**LPIPS**). | PSNR, SSIM, LPIPS. | PSNR, SSIM, LPIPS. | PSNR, SSIM, LPIPS, CIEDE2000. |
| **Giao thức tiền xử lý dữ liệu** | Crop ngẫu nhiên thành các patch kích thước 256×256 hoặc 128×128 pixel; chuẩn hóa pixel về dải $[0, 1]$. | Crop thành patch và resize về kích thước chuẩn. | Crop thành patch và huấn luyện trên độ phân giải gốc 384x284. | Do ảnh gốc có độ phân giải siêu cao (3K/4K), mô hình thường resize về 512×512 hoặc crop ngẫu nhiên patch kích thước lớn (e.g. 512x512) để duy trì bối cảnh tương phản. |
| **Hiệu năng Baseline (PSNR / SSIM)** | - **RetinexNet**: 16.77 dB / 0.560 <br>- **KinD**: 20.86 dB / 0.790 <br>- **Restormer**: 22.43 dB / 0.823 <br>- **Retinexformer**: **25.16 dB / 0.845** | - **RetinexNet**: 15.11 dB / 0.428 <br>- **KinD**: 17.56 dB / 0.702 <br>- **Restormer**: 19.85 dB / 0.756 <br>- **Retinexformer**: **21.50 dB / 0.785** | - **RetinexNet**: 18.23 dB / 0.635 <br>- **KinD**: 21.05 dB / 0.812 <br>- **Restormer**: 23.40 dB / 0.865 <br>- **Retinexformer**: **26.80 dB / 0.902** | - **RetinexNet**: 17.50 dB / 0.680 <br>- **KinD**: 19.30 dB / 0.760 <br>- **Cai et al.**: 19.50 dB / 0.800 <br>- **Retinexformer**: **22.10 dB / 0.835** |

---

> [!NOTE]
> **Nhận xét quan trọng:** 
> LOL (v1) mặc dù là benchmark kinh đoán nhưng có nhược điểm chí mạng là số lượng ảnh kiểm thử quá ít (15 ảnh) và có sự trùng lặp bối cảnh giữa tập train/test. LOL-v2 (Real) đã khắc phục xuất sắc nhược điểm này bằng cách phân tách độc lập bối cảnh và tăng mức độ thách thức về nhiễu thực tế. Trong khi đó, SICE mang tính đặc thù cao, kiểm tra khả năng phục hồi dải tương phản rộng (HDR-like) và xử lý phơi sáng không đều (non-uniform exposure) thay vì chỉ khử nhiễu tối đơn thuần.
