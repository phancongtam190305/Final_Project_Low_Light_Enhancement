# Phần 2: Tour Hướng Dẫn Đi Qua Paper (The Paper's Guided Tour Map)

Chào bạn! Hãy mở song song tệp PDF gốc [retinexformer.pdf](file:///d:/Desktop/tap%20tanh%20hoc%20code/.vscode/Summer_2026/Final_Project_Low_Light_Enhancement/docs/papers/retinexformer/retinexformer.pdf) bên cạnh màn hình của bạn. Tài liệu này sẽ đóng vai trò như một **hướng dẫn viên du lịch học thuật**, dắt tay bạn đi qua từng trang của bài báo để bạn nắm bắt thông tin nhanh và hiệu quả nhất!

---

## 🗺️ Hành Trình Khám Phá Paper Theo Từng Trang

```mermaid
journey
    title Hành Trình Đọc Paper Retinexformer
    section Trang 1-2: Nỗi đau & Ý tưởng
      Đọc Abstract: 5
      Nhìn Figure 1: 5
      Đọc Giới thiệu: 4
    section Trang 3-5: Trọng tâm Kỹ thuật
      Nhìn Figure 2 (Kiến trúc): 5
      Đọc Công thức (1) đến (6): 4
      Nhìn Figure 3 (Khối IG-MSA): 5
    section Trang 6-8: Chứng minh thực nghiệm
      Đọc Table 1 & 2 (Benchmark): 5
      Nhìn Figure 5 & 6 (So sánh ảnh): 4
      Đọc Table 3 & 4 (Bóc tách): 3
```

---

### 📍 Trạm Dừng Số 1: Trang 1 và Trang 2 - Đọc gì để hiểu "Nỗi Đau" & "Ý Tưởng"?

* **Điểm cần nhìn ngay lập tức**: **Figure 1 (Hình 1 - Trang 2)** ở góc trên bên phải.
  * *Hướng dẫn quan sát*: Tác giả vẽ sơ đồ so sánh 3 kiến trúc:
    * *(a) Hai giai đoạn truyền thống (RetinexNet style)*: Chia ảnh thành 2 nhánh độc lập để tăng sáng và khử nhiễu $\rightarrow$ Nhược điểm: Sai số nhánh này cộng dồn sang nhánh kia (Error propagation).
    * *(b) Mạng học sâu thông thường*: Học trực tiếp ánh xạ pixel $\rightarrow$ Nhược điểm: Bỏ qua quy luật vật lý Retinex, dễ bị loang màu.
    * *(c) Retinexformer (One-stage)*: **Khung màu đỏ**. Tác giả đưa cơ chế phân rã Retinex thẳng vào luồng xử lý của Transformer một cách đồng bộ trong một giai đoạn duy nhất $\rightarrow$ Ưu điểm: Khắc phục triệt để sai số lan truyền.
* **Đoạn văn cần đọc lướt**: Cột bên trái Trang 1 (Phần Abstract) để nắm bắt từ khóa cốt lõi, và đoạn cuối cùng của phần **1. Introduction (Trang 2)** - nơi tác giả liệt kê 3 dấu đầu dòng đóng góp của bài báo.

---

### 📍 Trạm Dừng Số 2: Trang 3, 4 và 5 - Trọng Tâm Kiến Trúc Kỹ Thuật (meticulous reading)

*Đây là khu vực học thuật "nặng đô" nhất của paper, chứa đựng toàn bộ bí quyết công nghệ làm nên giải thưởng ICCV.*

* **Hình vẽ quan trọng nhất bài báo**: **Figure 2 (Hình 2 - Trang 4)**.
  * *Hướng dẫn quan sát*: Đây là sơ đồ kiến trúc tổng thể của Retinexformer.
    1. Ảnh tối đầu vào $I$ đi qua khối **Illumination Estimator** (bộ ước lượng ánh sáng thô) để tạo ra bản đồ ánh sáng ban đầu.
    2. Sau đó, bản đồ này cùng với ảnh gốc được đưa vào chuỗi các khối **IGT (Illumination-Guided Transformer)** sắp xếp theo cấu trúc hình chữ U (U-Net style).
    3. Đầu ra là ảnh tăng sáng đẹp đẽ.
* **Hình vẽ khối Attention cốt lõi**: **Figure 3 (Hình 3 - Trang 5)**.
  * *Hướng dẫn quan sát*: Hình này phóng to khối chú ý **IG-MSA**. Bạn sẽ thấy ma trận ánh sáng (Illumination Representation) được ký hiệu bằng màu vàng cam, trực tiếp tham gia vào việc "dẫn đường" (nhân ma trận) với các đặc trưng khóa (Key) và truy vấn (Query) của ảnh để ra được bản đồ chú ý cuối cùng.
* **Các phương trình toán học cần lưu tâm (Trang 3 & 4)**:
  * Phương trình **Equation (5)** và **Equation (6)**: Công thức toán học định nghĩa cách phân rã Retinex một giai đoạn tích hợp thành phần nhiễu $C$.

---

### 📍 Trạm Dừng Số 3: Trang 6 và Trang 7 - Đọc số liệu Benchmark chứng minh sức mạnh

*Để thuyết phục hội đồng chấm đồ án tốt nghiệp, bạn phải biết cách trích dẫn số liệu thực nghiệm.*

* **Bảng số liệu định lượng**: **Table 1 (Bảng 1 - Trang 6)** và **Table 2 (Bảng 2 - Trang 7)**.
  * *Hướng dẫn quan sát*: 
    * Hãy nhìn vào dòng chữ in đậm **Retinexformer** ở cuối mỗi bảng.
    * So sánh điểm số **PSNR** và **SSIM** (càng cao càng tốt) và **LPIPS** (càng thấp càng tốt).
    * Bạn sẽ thấy trên tập **LOL-v1 (Table 1)**, Retinexformer đạt **28.92 dB PSNR** (cao nhất bảng), vượt xa mô hình Transformer nổi tiếng Restormer (22.72 dB) và các mô hình CNN khác.
* **Đoạn văn cần đọc**: Phần **4.2. Quantitative Comparison** để biết cách tác giả lập luận và chứng minh thuật toán của mình tốt hơn các thuật toán khác bằng con số cụ thể.

---

### 📍 Trạm Dừng Số 4: Trang 8 - So sánh trực quan (Thị giác người dùng)

* **Hình vẽ so sánh chất lượng ảnh**: **Figure 5 (Hình 5 - Trang 8)** và **Figure 6 (Hình 6 - Trang 9)**.
  * *Hướng dẫn quan sát*: Hãy zoom to Figure 5 lên 200%. Bạn sẽ nhìn thấy ảnh của Retinexformer (ở góc dưới cùng bên phải) có màu sắc cực kỳ tự nhiên, các vùng tối của tủ sách, hộp bút được làm sáng rõ chi tiết mà không hề bị loang lổ nhiễu hạt hay bị cháy sáng trắng như các phương pháp khác (ví dụ LIME bị cháy sáng, KinD bị mờ cạnh).
* **Nghiên cứu bóc tách (Ablation Study)**: **Table 3 (Trang 8)**. Chứng minh tính hiệu quả của khối **IG-MSA**. Nếu thay khối này bằng cơ chế Self-Attention thông thường, điểm PSNR lập tức rơi từ **28.92 dB xuống 27.56 dB**, chứng minh đóng góp của khối này là có giá trị thực sự chứ không phải lý thuyết suông.
