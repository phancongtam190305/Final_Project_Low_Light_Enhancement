# Phần 5: Đánh Giá Đồ Án & Đề Xuất Điểm Cải Tiến (Thesis Evaluation)

Tài liệu này đánh giá khách quan tiềm năng ứng dụng của **Retinexformer** dưới góc nhìn đồ án tốt nghiệp khoa học, đồng thời **đề xuất 2 hướng cải tiến cụ thể** giúp nhóm của bạn tạo điểm nhấn mới (novelty) để thuyết phục tuyệt đối hội đồng chấm đồ án.

---

## 📊 1. Đánh Giá Khách Quan Về Mô Hình Retinexformer

### 👍 Ưu điểm nổi bật (Sức mạnh khoa học)
* **Tính khoa học rất cao**: Việc kết hợp lý thuyết vật lý truyền thống (Retinex) vào cơ chế học sâu tối tân (Transformer) là một hướng đi cực kỳ đẹp mắt, được giới khoa học đánh giá rất cao về mặt tư duy nghiên cứu.
* **Chất lượng ảnh SOTA**: Đạt điểm số PSNR/SSIM cực kỳ ấn tượng trên các benchmark chuẩn (LOL dataset), ảnh khôi phục sạch nhiễu, biên sắc nét và không bị bệt màu.
* **Mã nguồn mở hoàn chỉnh**: Tác giả đã công bố code sạch sẽ trên GitHub, giúp việc tái cấu trúc và chạy thử nghiệm (reproduce) của nhóm bạn trở nên rất dễ dàng.

### 👎 Nhược điểm thực tế (Nút thắt cần giải quyết)
* **Gánh nặng tài nguyên (Compute-heavy)**: Mặc dù khối IG-MSA đã tối ưu hóa tuyến tính, Retinexformer vẫn rất nặng nề khi huấn luyện do cấu trúc Transformer chữ U sâu. Nhóm bạn sẽ cần một chiếc máy tính có GPU khỏe (VRAM từ 8GB trở lên như RTX 3060/3070/4060) để chạy thử nghiệm mượt mà.
* **Nguy cơ Overfitting**: Mạng có dung lượng tham số lớn, nếu huấn luyện trên tập dữ liệu nhỏ (như LOLv1 485 ảnh) mà không có cơ chế tăng cường dữ liệu (data augmentation) tốt sẽ rất dễ bị overfit (chỉ chạy tốt trên tập train, chạy tệ trên tập test ngoài đời thực).

---

## 💡 2. Hai Đề Xuất Cải Tiến Cụ Thế Làm Điểm Mới Cho Đồ Án

Để biến đồ án từ *"Cài đặt lại mô hình có sẵn"* thành *"Đề xuất cải tiến có đóng góp khoa học"*, nhóm bạn có thể chọn và triển khai 1 trong 2 hướng cải tiến rất thực tế dưới đây:

### 🌟 Ý tưởng 1: Phiên bản Siêu Nhẹ dùng Chưng Cất Tri Thức (Lightweight Retinexformer via Knowledge Distillation)
*Phù hợp nếu nhóm bạn muốn hướng tới ứng dụng thực tế chạy thời gian thực trên camera an ninh hoặc thiết bị nhúng.*

* **Đặt vấn đề**: Retinexformer gốc quá nặng để chạy trên các thiết bị biên (như Jetson Nano hoặc điện thoại di động).
* **Đề xuất cải tiến**:
  1. Nhóm bạn thiết kế một phiên bản Retinexformer rút gọn (giảm số lượng layer IGT, sử dụng Group Convolution thay cho tích chập thông thường) gọi là **Student Network** (Mạng học sinh - siêu nhẹ).
  2. Sử dụng kỹ thuật **Knowledge Distillation (Chưng cất tri thức)**: Cho mô hình Retinexformer gốc đã được huấn luyện thành công đóng vai trò **Teacher Network** (Mạng giáo viên).
  3. Huấn luyện mạng Student học theo các bản đồ đặc trưng (feature maps) và ma trận chú ý (attention maps) của mạng Teacher thông qua một hàm loss chưng cất bổ trợ ($\mathcal{L}_{distill}$).
* **Đóng góp của đồ án**: *"Đề xuất giải pháp chưng cất tri thức giúp tối ưu hóa và tăng tốc độ thời gian thực cho mạng Retinexformer ứng dụng trên thiết bị di động."* (Điểm cộng tuyệt đối từ hội đồng vì tính thực tiễn cao).

---

### 🌟 Ý tưởng 2: Khối Chú Ý Thích Ứng Không Gian Chống Cháy Sáng Cục Bộ (Spatially-Adaptive CBAM Integration)
*Phù hợp nếu nhóm bạn muốn đi sâu vào chất lượng hình ảnh của các cảnh đêm đô thị phức tạp.*

* **Đặt vấn đề**: Retinexformer đôi khi tăng sáng quá đà ở những vùng vốn đã có nguồn sáng mạnh sẵn (như đèn pha ô tô, bóng đèn đường trong đêm), gây ra hiện tượng cháy sáng gắt (over-exposure) làm mất chi tiết xung quanh nguồn sáng.
* **Đề xuất cải tiến**:
  1. Tích hợp thêm một khối chú ý không gian và kênh **Spatially-Adaptive CBAM** ở đầu vào của bộ IGT.
  2. Khối này sẽ tự động học một bản đồ trọng số phơi sáng. Tại những khu vực pixel có độ sáng vượt quá một ngưỡng $\tau$ (vùng đã đủ sáng), hệ số chú ý sẽ bị kìm hãm để chống tăng sáng quá đà. Các vùng tối sâu còn lại sẽ được kích hoạt tăng sáng tối đa.
  3. Kết hợp với hàm loss chống cháy sáng cục bộ để tối ưu hóa đồng thời.
* **Đóng góp của đồ án**: *"Cải tiến mô hình Retinexformer bằng khối chú ý thích ứng không gian giúp bảo toàn độ trung thực màu sắc và chống cháy sáng cục bộ cho cảnh đêm đô thị phức tạp."* (Ghi điểm xuất sắc vì giải quyết được một điểm mù thực tế lớn của paper gốc).
