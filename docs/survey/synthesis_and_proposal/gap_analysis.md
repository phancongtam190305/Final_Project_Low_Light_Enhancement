# Báo Cáo Phân Tích Khoảng Trống Nghiên Cứu Tổng Thể (Master Gap Analysis)

Tài liệu này tổng hợp toàn bộ kết quả khảo sát từ 5 nhánh của bài toán **Low-Light Image Enhancement (LLIE)**, thực hiện so sánh đối chiếu đa chiều nhằm chỉ ra những nút thắt kỹ thuật (bottlenecks) và các khoảng trống nghiên cứu (gaps) còn mở. Đây là cơ sở cốt lõi giúp nhóm của bạn định hình tính mới (novelty) cho đồ án tốt nghiệp.

---

## 📊 1. Bảng So Sánh Đa Chiều Giữa 5 Nhánh Nghiên Cứu

Dưới đây là bảng tổng hợp so sánh định lượng và định tính giữa 5 nhánh dựa trên kết quả khảo sát từ các subagents chuyên trách:

| Tiêu Chí So Sánh | Nhánh 1: Paired RGB | Nhánh 2: Unpaired / Zero-Ref | Nhánh 3: RAW Low-Light | Nhánh 4: Real-world High-Res | Nhánh 5: Downstream Task |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bản chất kỹ thuật** | Học giám sát ánh xạ pixel-to-pixel dựa trên ảnh cặp. | Học không giám sát bằng GAN hoặc hàm loss vật lý / ước lượng đường cong. | Xử lý dữ liệu thô cảm biến (Bayer), thay thế ISP phần cứng bằng Deep ISP. | Tăng sáng ảnh siêu phân giải (2K/4K) phơi sáng không đều và phức tạp. | Tăng cường ảnh làm đầu vào bổ trợ cho mô hình nhận diện (YOLO/Segmenter). |
| **Dataset chủ lực** | [LOL](https://daooshee.github.io/RetinexNet/), [LOL-v2](https://github.com/flyywh/Awesome-Low-Light-Enhancement), [SICE](https://github.com/csjcai/SICE) | [DICM](https://github.com/Li-Chongyi/Zero-DCE), [LIME](https://github.com/weichen582/LIME), [MEF](https://github.com/Li-Chongyi/Zero-DCE) | [SID](https://cchen156.github.io/SeeInTheDark.html), [SDSD](https://github.com/flyywh/Awesome-Low-Light-Enhancement), [SMID](https://github.com/flyywh/Awesome-Low-Light-Enhancement) | [NTIRE 2024/2025](https://github.com/cvpr-ntire-llie) | [ExDark](https://github.com/cs-chan/Exclusively-Dark-Image-Dataset), [LLVIP](https://bupt-ai-cz.github.io/LLVIP/), [LoLI-Street](https://github.com/tanvirnwu/TriFuse) |
| **Yêu cầu Ground Truth** | Bắt buộc phải có cặp ảnh tối/sáng tĩnh hoàn hảo. | Hoàn toàn không cần (Zero-Reference) hoặc dùng ảnh không cặp. | Bắt buộc phải có (ảnh chụp phơi sáng dài làm GT). | Bắt buộc phải có (được căn chỉnh quang-cơ học chính xác). | Tùy chọn (dùng ảnh cặp hoặc không), nhưng cần nhãn hạ nguồn (YOLO label). |
| **Metrics đánh giá** | Định lượng: PSNR, SSIM, LPIPS. | Định tính: NIQE, BRISQUE, User Study. | Định lượng (tính trên sRGB): PSNR, SSIM, LPIPS. | Định lượng & Định tính: PSNR, SSIM, LPIPS, NIQE. | Định lượng ứng dụng: **mAP** (Detection), **mIoU** (Segmentation). |
| **Mức độ chín muồi** | Đã bão hòa (Đạt PSNR ~28dB+ trên LOL). | Khá chín muồi cho ứng dụng di động/thực tế. | Đang phát triển mạnh trong công nghiệp máy ảnh. | Mới nổi, là thách thức cao nhất hiện tại. | Cực kỳ nóng (hot-topic), còn nhiều không gian mở. |
| **Tài nguyên GPU yêu cầu** | Vừa phải đến Khá. | Rất nhẹ (phù hợp máy cấu hình yếu). | Rất cao (VRAM >12GB/24GB). | Cao (Xử lý 4K dễ tràn VRAM). | Khá cao (Phải chạy cả mô hình LLIE + YOLO). |
| **Độ khả thi làm Đồ án** | **Cực kỳ an toàn (5/5)** nhưng khó đột phá. | **Rất khả thi (4.5/5)**, thích hợp demo thực tế. | **Khó thực hiện (3.5/5)**, thích hợp nghiên cứu sâu. | **Thách thức (3.5/5)**, phù hợp nhóm học lực tốt. | **Xuất sắc (4.5/5)**, dễ ghi điểm tuyệt đối. |

---

## 🔍 2. Năm Khoảng Trống Nghiên Cứu Lớn (Consolidated Gaps) Đáng Khai Thác

Dựa trên phân tích sâu từ các báo cáo nhánh, chúng tôi đã tổng hợp thành **5 khoảng trống nghiên cứu cốt lõi** mà nhóm của bạn có thể chọn làm điểm cải tiến (contribution) cho đồ án:

### 🔴 Gap 1: Sự sụp đổ năng lực tổng quát hóa (Domain Shift & Cross-Dataset Barrier)
* **Vấn đề**: Hầu hết các mô hình SOTA được huấn luyện trên LOL Dataset (ảnh trong nhà, tối đều) khi mang sang chạy thử trên ảnh đêm ngoài đường phố thực tế (DICM/LIME) đều bị sụt giảm chất lượng nghiêm trọng (lệch màu sắc, bệt chi tiết, nhiễu loang lổ).
* **Cơ hội cho đồ án**: Thiết kế một phương pháp huấn luyện thích ứng miền không giám sát (Unsupervised Domain Adaptation) hoặc một bộ sinh ảnh thiếu sáng nhân tạo dựa trên vật lý (physics-based low-light simulator) để huấn luyện mô hình có độ bền bỉ cao trên thực tế.

### 🔴 Gap 2: Sự xung đột giữa Tăng sáng và Phóng đại nhiễu cảm biến (Noise-Enhancement Entanglement)
* **Vấn đề**: Trong môi trường thiếu sáng sâu, tín hiệu ảnh bị lấn át bởi nhiễu cảm biến (read noise, shot noise). Các thuật toán tăng sáng thông thường nếu tăng độ sáng lên bao nhiêu lần thì sẽ khuếch đại nhiễu lên bấy nhiêu lần, gây ra hiện tượng loang lổ màu (chroma noise) rất xấu xí ở vùng tối.
* **Cơ hội cho đồ án**: Tích hợp các bộ lọc nhiễu tự thích ứng (noise-aware filters) hoặc sử dụng kiến trúc chú ý kênh (Channel Attention) để tách biệt bản đồ ánh sáng (illumination map) và bản đồ nhiễu (noise map), từ đó tăng sáng đi đôi với triệt tiêu nhiễu sâu.

### 🔴 Gap 3: Sự bất đối xứng giữa "Thị giác Con người" và "Thị giác Ngữ nghĩa của Máy" (Human Aesthetics vs. Machine Semantics)
* **Vấn đề**: Các hàm loss truyền thống như MSE hay $L_1$ có xu hướng làm mượt (smooth) các pixel để đạt điểm PSNR/SSIM cao. Việc làm mượt này làm mất đi các chi tiết tần số cao (cạnh, biên, kết cấu vật thể), làm ảnh trông đẹp với mắt người nhưng lại khiến các mô hình hạ nguồn như YOLO hay Segmenter bị mù đặc trưng ngữ nghĩa, dẫn đến sụt giảm mAP nghiêm trọng.
* **Cơ hội cho đồ án**: Đối với hướng Downstream, hãy thiết kế một hàm loss phản hồi ngữ nghĩa (Semantic Feedback Loss) được trích xuất trực tiếp từ đặc trưng của mạng YOLO để định hướng mô hình tăng sáng khôi phục đúng các vùng cạnh biên quan trọng của vật thể.

### 🔴 Gap 4: Điểm mù cân bằng sáng cục bộ và hiện tượng cháy sáng gắt (Local Exposure & Halo Artifacts)
* **Vấn đề**: Các bức ảnh đêm thực tế ngoài đường phố thường có độ chiếu sáng phi đồng nhất (non-uniform illumination) - ví dụ: xen kẽ giữa các vùng tối sâu là các vùng sáng gắt của đèn pha xe, đèn đường, bảng hiệu. Các mô hình LLIE thông thường nếu tăng sáng toàn cục (global enhancement) sẽ làm cháy hoàn toàn (over-exposure) các vùng sáng này, tạo ra các vầng hào quang giả (halo artifacts).
* **Cơ hội cho đồ án**: Thiết kế mô hình học cách ước lượng các đường cong điều chỉnh ánh sáng thích ứng không gian (Spatially-adaptive curves) hoặc sử dụng cơ chế Attention phân chia vùng sáng/tối để tăng sáng chọn lọc (chỉ tăng vùng tối, kìm hãm vùng sáng).

### 🔴 Gap 5: Rào cản VRAM phi mã và khả năng triển khai thời gian thực (The Edge Deployment Barrier)
* **Vấn đề**: Các kiến trúc SOTA sử dụng mạng Transformer (như Restormer, Retinexformer) đạt điểm PSNR cực cao nhưng có kích thước tham số khổng lồ và tốn VRAM khủng khiếp. Chúng hoàn toàn không thể chạy thời gian thực trên camera an ninh hay thiết bị nhúng (Jetson Nano) của xe tự lái.
* **Cơ hội cho đồ án**: Nghiên cứu kỹ thuật chưng cất tri thức (Knowledge Distillation) truyền tri thức từ "giáo viên" nặng nề (Retinexformer) sang mạng "học sinh" siêu nhẹ (Zero-DCE hoặc SCI), hoặc cải tiến mô hình Zero-DCE++ để vừa giữ được tốc độ >50 FPS vừa nâng cao chất lượng khôi phục màu sắc.

---

## 📈 3. Tổng Hợp Đánh Giá Độ Khó & Tiềm Năng Khai Thác Dataset

Dưới đây là điểm số trung bình (thang điểm 5) tổng hợp từ các đánh giá chuyên sâu của subagents cho các dataset tiêu biểu:

| Tên Dataset | Realism (Độ thực tế) | Diversity (Đa dạng) | Ground Truth Quality (Chất lượng GT) | Benchmark Maturity (Độ trưởng thành) | Gap Potential (Tiềm năng khai thác) | Điểm Trung Bình | Nhận Xét Chiến Lược |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LOL v1** | 3.0 | 2.0 | 4.0 | **5.0** | 2.0 | 3.00 | Đã quá cũ và bão hòa. Chỉ nên dùng làm baseline bắt buộc. |
| **LOL-v2 Real** | 4.0 | 3.5 | 4.0 | 4.0 | 3.5 | 3.83 | Bộ benchmark RGB chính thức tốt nhất hiện tại. |
| **SID (Sony RAW)** | 4.5 | 3.0 | 4.5 | 4.5 | 4.0 | 4.08 | Tuyệt vời cho hướng RAW học thuật sâu, nhưng rất nặng. |
| **NTIRE 2024** | **5.0** | **4.5** | 4.0 | 3.0 | **5.0** | **4.43** | Dataset thách thức nhất cho ảnh 4K thực tế. |
| **ExDark** | **5.0** | **4.5** | 1.0 (No GT) | 4.0 | **5.0** | 4.08 | Tiêu chuẩn vàng cho Object Detection ban đêm. |
| **LLVIP** | 4.5 | 3.5 | **5.0** | 3.5 | 4.0 | 4.08 | Rất độc đáo nếu muốn làm fusion RGB-Hồng ngoại. |
| **LoLI-Street** | 4.5 | 4.0 | 4.0 | 3.0 | **4.5** | 4.00 | Dataset rất mới (ACCV 2024), cực kỳ nhiều tiềm năng khai thác. |
