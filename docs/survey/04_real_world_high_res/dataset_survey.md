# Khảo Sát Chi Tiết Các Bộ Dữ Liệu Real-world High-Res (NTIRE 2024 & NTIRE 2025)

Trong những năm gần đây, bài toán Tăng cường ảnh thiếu sáng (LLIE) đã dịch chuyển mạnh mẽ từ các điều kiện lý thuyết (ảnh nhỏ, tối đều) sang các thách thức thực tế ngoài đời thực: **Độ phân giải siêu cao (2K/4K/8K)**, **ánh sáng không đồng đều (non-uniform illumination)**, **ngược sáng (backlight)**, và **độ tương phản động cực cao (high dynamic range)**. Đi đầu trong xu hướng này là các cuộc thi danh giá tại hội nghị CVPR thông qua các thử thách NTIRE (New Trends in Image Restoration and Enhancement). Tài liệu này cung cấp bảng khảo sát chi tiết hệ thống hai bộ dữ liệu thực tế và độ phân giải cao nổi bật nhất: **NTIRE 2024 LLIE Dataset** và **NTIRE 2025 LLIE Dataset**.

---

## 📊 Bảng 1: Thông Tin Cơ Bản (Basic Information)

Bảng này cung cấp cái nhìn tổng quan về nguồn gốc, quy mô, định dạng dữ liệu và mục đích thiết kế của các bộ dữ liệu NTIRE High-Res.

| Tiêu Chí Đánh Giá | NTIRE 2024 LLIE Dataset | NTIRE 2025 LLIE Dataset |
| :--- | :--- | :--- |
| **Tác giả & Ban tổ chức** | Ban tổ chức NTIRE 2024 (CVPR Workshops 2024) | Ban tổ chức NTIRE 2025 (CVPR Workshops 2025) |
| **Loại dữ liệu (Data Type)** | High-Resolution sRGB RGB (Độ phân giải thực tế cao) | Ultra-High-Resolution sRGB RGB (Độ phân giải siêu cao) |
| **Quy mô mẫu (Quantity)** | Tổng cộng **300 cảnh** thực tế cặp được chọn lọc kỹ lưỡng. | Tổng cộng **295 cảnh** thực tế phức tạp và độ phân giải siêu nét. |
| **Cấu trúc cặp (Paired/Unpaired)** | Paired (Cặp ảnh thiếu sáng phơi sáng ngắn và ảnh đủ sáng chuẩn). | Paired (Cặp ảnh thiếu sáng phơi sáng ngắn và ảnh đủ sáng chuẩn). |
| **Bối cảnh miền (Domain/Context)** | Các cảnh đêm thực tế đa dạng: Đô thị, trong nhà, ngoài trời, ngược sáng mạnh, ánh sáng hỗn hợp phi tuyến tính. | Cảnh đêm đô thị có độ tương phản cực đoan, điều kiện thời tiết phức tạp, ánh sáng neon nhiều màu sắc, nội thất thiếu sáng sâu. |
| **Độ phân giải (Resolution)** | Siêu phân giải: Từ **2K đến 4K** trở lên (ví dụ: $3840 \times 2160$, $4000 \times 3000$). | Siêu phân giải: **4K và vượt 4K** (UHD và Ultra-HD+, độ phân giải pixel cực lớn). |
| **Phân chia dữ liệu (Train/Val/Test)** | - Huấn luyện (Train): 230 cảnh.<br>- Xác thực (Val): 35 cảnh.<br>- Kiểm thử (Test): 35 cảnh. | - Huấn luyện (Train): 219 cảnh.<br>- Xác thực (Val): 46 cảnh.<br>- Kiểm thử (Test): 30 cảnh. |
| **Nguồn tải & Giấy phép** | [NTIRE 2024 GitHub](https://github.com/cvpr-ntire-llie) (CC BY-NC 4.0 - Academic Only) | [NTIRE 2025 GitHub](https://github.com/cvpr-ntire-llie) (CC BY-NC 4.0 - Academic Only) |

---

## ⚙️ Bảng 2: Đặc Tính Kỹ Thuật (Technical Characteristics)

Bảng này đi sâu vào khía cạnh phần cứng cảm biến, cấu hình thiết lập khi thu thập dữ liệu và các thách thức đặc thù về nhiễu vật lý của mỗi dataset.

| Đặc Tính Kỹ Thuật | NTIRE 2024 LLIE Dataset | NTIRE 2025 LLIE Dataset |
| :--- | :--- | :--- |
| **Thiết bị thu thập dữ liệu** | Chụp bằng các máy ảnh DSLR chuyên nghiệp (Sony, Canon, Nikon) kết hợp chân máy chống rung và thiết lập phơi sáng thủ công. | Máy ảnh chuyên nghiệp cao cấp với cảm biến full-frame khổ lớn nhằm giữ nguyên chi tiết biên và tần số cao ở độ phân giải 4K. |
| **Điều kiện chiếu sáng** | Ánh sáng phi đồng nhất: Vùng tối sâu bên cạnh vùng sáng chói (neon, đèn đường). Nhiều cảnh ngược sáng (backlight) thử thách khả năng cân bằng sáng. | Độ tương phản động siêu cao (Ultra-HDR): Thử thách tối cực đoan (gần như 0 lux ở góc tối) và cháy sáng cục bộ mạnh (đèn pha ô tô, biển hiệu LED). |
| **Độ phân giải & Tỷ lệ** | 2K/4K thực tế, bảo tồn tuyệt đối các chi tiết vân bề mặt (texture) tinh tế. | Siêu phân giải 4K+, mật độ chi tiết biên cực lớn, dung lượng file ảnh nén sRGB rất lớn (từ 15MB - 30MB/ảnh PNG). |
| **Định dạng file & Bit-depth** | `.png` (8-bit sRGB chuẩn hóa màu, không nén mất chi tiết). | `.png` (8-bit hoặc 16-bit sRGB chuẩn hóa màu chất lượng cao). |
| **Đặc điểm nhiễu (Noise)** | Nhiễu hạt sRGB dạng Gaussian-Poisson phức tạp sau ISP, nhiễu nén nhẹ, mất mát màu sắc và độ bão hòa ở vùng tối. | Nhiễu màu (chrominance noise) loang lổ vùng tối sâu, mất chi tiết vân tần số cao, nhiễu mờ do khí quyển hoặc bụi đêm. |
| **Thách thức kỹ thuật cốt lõi** | - Tăng sáng vùng tối sâu mà không làm cháy sáng (over-exposure) vùng sáng sẵn.<br>- Khử nhiễu sRGB loang lổ mà không làm bệt các chi tiết 4K. | - Giới hạn bộ nhớ VRAM GPU khi huấn luyện mô hình với ảnh 4K.<br>- Duy trì độ chân thực màu sắc (color fidelity) không bị biến dạng màu (color cast) dưới ánh sáng neon phức tạp. |

---

## 🔬 Bảng 3: Protocol & Đánh Giá (Protocol & Evaluation)

Bảng này phân tích các bước xử lý dữ liệu trước khi đưa vào mạng huấn luyện, các siêu tham số tiêu chuẩn và quy trình đánh giá kết quả.

| Tiêu Chí Quy Trình | NTIRE 2024 LLIE Dataset | NTIRE 2025 LLIE Dataset |
| :--- | :--- | :--- |
| **Căn chỉnh cặp ảnh (Alignment)** | Các cặp ảnh được chụp tĩnh bằng tripod. Tuy nhiên, sai lệch sub-pixel do gió hoặc chuyển động nhỏ của lá cây vẫn được căn chỉnh bằng thuật toán so khớp đặc trưng (SIFT/ORB) và biến đổi đồng dạng (Homography). | Được kiểm soát nghiêm ngặt hơn bằng các hệ thống rig chắc chắn, kết hợp kiểm duyệt thủ công từng ảnh để loại bỏ hoàn toàn các cặp ảnh bị lệch góc hoặc mờ do rung tay. |
| **Thiết lập huấn luyện tiêu chuẩn** | - Do giới hạn bộ nhớ GPU, các phương pháp bắt buộc phải huấn luyện dạng **Patch-based**: Cắt ảnh thành các patch kích thước $256 \times 256$ hoặc $512 \times 512$.<br>- Optimizer: Adam / AdamW ($LR = 10^{-4}$ với Cosine Annealing).<br>- Epochs: 100 - 300 epochs. | - Huấn luyện Patch-based chất lượng cao, thường áp dụng các kỹ thuật tăng cường dữ liệu (Data Augmentation) mạnh mẽ để tránh overfit.<br>- Kích thước patch thường lớn hơn ($512 \times 512$ hoặc $1024 \times 1024$) để học các mối quan hệ không gian xa trên ảnh 4K. |
| **Chỉ số xếp hạng chính (Final Rank)** | Xếp hạng dựa trên công thức kết hợp trọng số:<br>$$\text{Final Rank} = 0.60 \times \text{Hạng PSNR} + 0.40 \times \text{Hạng SSIM}$$<br>(Chỉ số LPIPS được sử dụng làm tiêu chí phụ để phá vỡ các trường hợp hòa điểm). | Xếp hạng dựa trên công thức đánh giá toàn diện hơn:<br>$$\text{Final Rank} = 0.50 \times \text{PSNR} + 0.50 \times \text{SSIM}$$<br>kết hợp đánh giá sâu về cảm nhận thị giác thông qua **LPIPS** (40% trọng số phụ) và chỉ số chất lượng không tham chiếu **NIQE** (20% trọng số phụ). |
| **Quy trình kiểm thử & Nộp bài** | Người tham gia chạy suy diễn trên tập Test che nhãn (Ground Truth ẩn) và nộp kết quả ảnh đã tăng cường lên server CodaLab để tính điểm tự động. | Chạy suy diễn trên tập Test ẩn hoàn toàn, nộp kết quả lên CodaLab. Ban tổ chức kiểm tra chéo mã nguồn của các đội dẫn đầu để đảm bảo tính minh bạch và khả năng tái lặp. |
| **Đầu ra mong muốn (Target)** | Ảnh tăng cường sáng tự nhiên, giữ nguyên cấu trúc vật thể, không bị cháy sáng ở các nguồn đèn, biên sắc nét ở độ phân giải 4K. | Ảnh có độ tương phản hài hòa cao, khử sạch nhiễu hạt vùng tối mà không làm nhòe vân bề mặt, khôi phục màu sắc rực rỡ và chân thực như chụp ban ngày. |
