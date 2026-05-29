# Điểm Chuẩn Thuật Toán & Phân Tích Khoảng Trống Nghiên Cứu: Real-world High-Res

Tài liệu này tổng hợp các kết quả thực nghiệm và xếp hạng SOTA trên hai bộ dữ liệu độ phân giải cao thực tế tiêu chuẩn: **NTIRE 2024 LLIE** và **NTIRE 2025 LLIE**. Tiếp theo, tài liệu thực hiện đánh giá độ khó của các bộ dữ liệu này thông qua 7 tiêu chí khoa học, đồng thời phân tích sâu sắc 3 khoảng trống nghiên cứu lớn (gaps) mà các nhà nghiên cứu LLIE thế hệ mới cần tập trung giải quyết.

---

## 📊 Bảng 1: Bảng So Sánh Các Phương Pháp (Method Comparison)

Bảng dưới đây trình bày kết quả thực nghiệm của các đội thi dẫn đầu và các phương pháp SOTA tiêu biểu trên tập dữ liệu kiểm thử **NTIRE 2024 / NTIRE 2025 LLIE Challenge**:

| Tên Phương Pháp / Đội Thi | Loại Kiến Trúc | Bộ Dữ Liệu Thử Nghiệm | PSNR (dB) ↑ | SSIM ↑ | LPIPS ↓ | Đặc Trưng Kiến Trúc & Giải Pháp Kỹ Thuật | Trạng Thái / Link Mã Nguồn |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SYSU-FVL-T2** (Vô địch NTIRE 2024) | CNN nâng cao (ESDNet-L) | NTIRE 2024 Test | **25.52** | **0.8637** | **0.245** | Sử dụng mạng ESDNet-L làm backbone, kết hợp cấu trúc đa quy mô (multi-scale), kỹ thuật progressive training và tăng cường dữ liệu cực mạnh. | [SYSU Repo](https://github.com/cvpr-ntire-llie) |
| **Retinexformer** (SOTA Baseline) | Transformer + Retinex | NTIRE 2024 Test | 25.30 | 0.8525 | 0.258 | Phân rã ảnh dựa trên lý thuyết Retinex kết hợp với cơ chế OR-Attention (One-stage Retinex-based Attention), cân bằng xuất sắc giữa khử nhiễu và bảo tồn cấu trúc. | [Retinexformer Code](https://github.com/caiyuanhao1998/Retinexformer) |
| **DH-AISP** (Hạng 3 NTIRE 2024) | Mạng Hai Nhánh (Two-Branch) | NTIRE 2024 Test | 24.97 | 0.8528 | 0.262 | Sử dụng phép biến đổi Walsh (Discrete Walsh Transform - DWT) để tách biệt thông tin tần số cao, kết hợp đặc trưng trích xuất từ ConvNeXt. | [DH-AISP Paper](https://github.com/cvpr-ntire-llie) |
| **LVGroup HFUT** (Top 4 NTIRE 2024) | CNN lai Transformer | NTIRE 2024 Test | 24.88 | 0.8395 | 0.280 | Thiết kế luồng xử lý song song để khôi phục nhanh các vùng ảnh lớn 4K mà không làm suy giảm cấu trúc biên của vật thể. | [LVGroup Repo](https://github.com/cvpr-ntire-llie) |
| **NWPU-DiffLight** (Top 5 NTIRE 2024) | Mô hình Khuếch Tán (Diffusion Model) | NTIRE 2024 Test | 24.78 | 0.8556 | 0.230 | Tích hợp thuật toán khuếch tán để sinh ra các chi tiết bề mặt (texture) thực tế hơn, đạt chỉ số LPIPS (perceptual) rất ấn tượng nhưng PSNR bị kéo giảm nhẹ. | [NWPU Repo](https://github.com/cvpr-ntire-llie) |
| **Restormer Baseline** (Zamir et al., 2022) | Transformer thuần túy | NTIRE 2024 Test | 23.40 | 0.8100 | 0.320 | Áp dụng cơ chế chú ý tự tương quan kênh chéo. Rất mạnh về khử nhiễu nhưng chi phí tính toán cực kỳ lớn khi chạy trên ảnh độ phân giải 4K gốc. | [Restormer Code](https://github.com/swz30/Restormer) |
| **SCI (Self-Calibrated)** (Li et al., CVPR 2022) | Học không giám sát (Zero-shot) | NTIRE 2024 Test | 18.50 | 0.7200 | 0.450 | Kiến trúc siêu nhẹ, suy diễn thời gian thực cực nhanh nhưng thất bại trong việc khử nhiễu hạt loang lổ vùng tối sâu của ảnh 4K. | [SCI Repo](https://github.com/Li-Chongyi/SCI) |

---

## 📈 Bảng 2: Bảng Chấm Điểm Độ Khó Của Dataset (Difficulty Ratings)

Thang điểm đánh giá độ khó và tính khoa học của hai bộ dữ liệu từ **1 (Rất dễ)** đến **5 (Xuất sắc / Cực khó)**:

| Tiêu Chí Đánh Giá | NTIRE 2024 LLIE Dataset | NTIRE 2025 LLIE Dataset | Nhận Xét / Biện Giải Khoa Học |
| :--- | :---: | :---: | :--- |
| **1. Tính thực tế (Realism)** | 5.0 | 5.0 | Cả hai bộ dữ liệu đều sử dụng các bức ảnh chụp thực tế từ các cảm biến cao cấp ngoài phố đêm, phản ánh chính xác các hiện tượng quang học thực. |
| **2. Độ đa dạng (Diversity)** | 4.5 | 4.8 | NTIRE 2025 có độ đa dạng bối cảnh vượt trội hơn với sự xuất hiện của các điều kiện thời tiết phức tạp (mưa, sương mù nhẹ) và ánh sáng đô thị hỗn hợp. |
| **3. Độ khó tác vụ (Difficulty)** | 4.5 | 5.0 | NTIRE 2025 tăng đáng kể độ khó bằng việc đưa vào các cảnh tối sâu (gần 0 lux) đi kèm các nguồn đèn pha công suất lớn gây chênh lệch sáng cực đoan. |
| **4. Chất lượng Ground Truth** | 4.5 | 4.8 | NTIRE 2025 áp dụng quy trình kiểm duyệt thủ công nghiêm ngặt và hệ thống rig camera cố định tuyệt đối, giảm thiểu sai lệch dịch chuyển sub-pixel tốt hơn. |
| **5. Độ trưởng thành Benchmark** | 4.5 | 4.0 | NTIRE 2024 đã được sử dụng rộng rãi và có nhiều bài báo công bố so sánh trực tiếp. NTIRE 2025 là benchmark mới nhất, đang trong giai đoạn bùng nổ nghiên cứu. |
| **6. Khả năng tái lặp (Reproducibility)**| 4.0 | 3.8 | Rất thách thức. Việc tái lặp các kết quả SOTA của cả hai bộ dữ liệu đòi hỏi hạ tầng phần cứng GPU cực mạnh (thường là cụm nhiều GPU A100/H100) để huấn luyện. |
| **7. Tiềm năng khai phá (Gap potential)**| 4.0 | 4.8 | Cực kỳ rộng mở. Các nghiên cứu tiếp theo có thể tập trung vào việc nén mô hình để chạy thời gian thực trên di động mà vẫn giữ được chất lượng 4K. |
| **Điểm Trung Bình (Average)** | **4.43** | **4.60** | **Bộ dữ liệu NTIRE 2025 đại diện cho tiêu chuẩn thử thách cao nhất hiện nay đối với bài toán tăng cường ảnh thực tế độ phân giải siêu cao.** |

---

## 🔍 Phân Tích Chuyên Sâu 3 Khoảng Trống Nghiên Cứu (Research Gaps)

### 1. Khoảng trống 1: Sự bùng nổ bộ nhớ VRAM GPU và rào cản triển khai thực tế trên thiết bị biên (Edge Deployment)
*   **Bản chất vấn đề:** Ảnh độ phân giải 4K chứa tới hơn 8 triệu điểm ảnh ($3840 \times 2160$). Các mô hình học sâu hiện đại như Vision Transformers (ViT) có độ phức tạp tính toán về mặt không gian tăng theo cấp số nhân ($O(N^2)$ với $N$ là số lượng pixel/patch).
*   **Hậu quả kỹ thuật:** Việc huấn luyện trực tiếp trên ảnh 4K gốc là bất khả thi trên các GPU thương mại thông thường do tràn VRAM. Khi áp dụng kỹ thuật cắt ảnh thành các patch nhỏ để huấn luyện, mô hình bị mất đi khả năng học thông tin phân phối ánh sáng toàn cục (global illumination context). Khi ghép ảnh đầu ra thường xuất hiện lỗi ranh giới patch hoặc ánh sáng không đều giữa các vùng. Ngoài ra, tốc độ suy diễn (inference latency) của các mô hình SOTA hiện nay mất từ vài giây đến hàng chục giây cho một ảnh 4K, hoàn toàn bất khả thi cho các tác vụ thời gian thực trên camera an ninh hoặc điện thoại thông minh.
*   **Hướng giải quyết khả thi:** Nghiên cứu các cơ chế chú ý tuyến tính (Linear Attention) hoặc ứng dụng kiến trúc **Mamba (State Space Models - SSMs)** có độ phức tạp tuyến tính $O(N)$ để xử lý trực tiếp ảnh 4K. Phát triển các mô hình chưng cất tri thức (Knowledge Distillation) nén mạng nơ-ron sâu thành các mô hình CNN siêu nhẹ chạy trên NPU của thiết bị di động.

### 2. Khoảng trống 2: Sự xung đột sâu sắc giữa tối ưu hóa định lượng (PSNR/SSIM) và chất lượng cảm nhận thị giác (Perceptual Quality)
*   **Bản chất vấn đề:** Các hàm mất mát truyền thống như L1 Loss hay MSE Loss hướng tới việc tối đa hóa chỉ số toán học **PSNR** và **SSIM** bằng cách tính trung bình sai lệch pixel. Lối tối ưu này vô tình phạt nặng các chi tiết tần số cao, dẫn đến việc mô hình có xu hướng làm mịn quá mức bức ảnh (hiện tượng bệt màu, mờ nhòe chi tiết vân bề mặt).
*   **Hậu quả kỹ thuật:** Trong thực tế, một bức ảnh đạt điểm PSNR rất cao (ví dụ 26 dB) trông có thể cực kỳ bệt, thiếu sức sống và không tự nhiên đối với mắt người. Ngược lại, các mô hình sử dụng hàm mất mát cảm nhận (Perceptual Loss, GAN Loss, Diffusion) tạo ra bức ảnh trông rất sắc nét, sống động (đạt điểm LPIPS tốt) nhưng chỉ số PSNR lại rất thấp do mô hình tự sinh ra các chi tiết giả tạo (hallucinations) lệch vài pixel so với Ground Truth.
*   **Hướng giải quyết khả thi:** Thiết kế các hàm mất mát tối ưu hóa đa mục tiêu động (Multi-Objective Optimization), tự động điều chỉnh trọng số giữa MSE, LPIPS và các chỉ số phi tham chiếu như NIQE tùy thuộc vào đặc trưng tần số của từng vùng ảnh (vùng phẳng vs vùng chứa nhiều chi tiết).

### 3. Khoảng trống 3: Cân bằng sáng cục bộ và bảo vệ màu sắc dưới ánh sáng phi đồng nhất (Local Exposure & Color Fidelity)
*   **Bản chất vấn đề:** Ảnh đêm thực tế không tối đều. Chúng thường chứa đồng thời các vùng tối sâu (shadows) và các vùng rất sáng (highlights) từ biển hiệu LED, đèn pha xe cộ hoặc đèn đường. 
*   **Hậu quả kỹ thuật:** Hầu hết các mô hình LLIE hiện tại khi cố gắng tăng sáng vùng tối sâu sẽ vô tình làm **cháy sáng hoàn toàn** (over-exposure) các vùng vốn đã đủ sáng, làm mất đi các chi tiết quan trọng (ví dụ: chữ trên biển hiệu, cấu trúc đèn). Ngược lại, nếu cố gắng kìm hãm vùng sáng, vùng tối lại không được tăng sáng đủ. Thêm vào đó, việc khôi phục màu sắc dưới ánh sáng phức tạp nhiều màu (như đèn neon) thường gây ra hiện tượng lệch màu (color cast) khiến bức ảnh trông thiếu tự nhiên và kỳ dị.
*   **Hướng giải quyết khả thi:** Tích hợp các bộ lọc phân tách tần số hoặc bản đồ hướng dẫn độ sáng cục bộ (Local Illumination Guide Map) để mạng nơ-ron học cách tăng sáng thích ứng theo từng vùng (Spatially-varying Enhancement). Áp dụng các không gian màu phân tách độ sáng và màu sắc (như LAB hoặc HSV) để mạng tối ưu hóa độc lập kênh độ sáng và kênh màu sắc.
