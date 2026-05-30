# Phần 4: Các Công Thức Toán Học & Hàm Loss (Math & Losses)

Để viết được chương **Cơ sở lý thuyết** trong quyển đồ án tốt nghiệp một cách xuất sắc, bạn cần giải thích được bản chất toán học của mô hình. Tài liệu này sẽ bóc tách chi tiết các công thức Retinex cải tiến và các hàm Loss tối ưu hóa của **Retinexformer** dưới dạng ký hiệu $LaTeX$ trực quan.

---

## 📐 1. Toán Học Phân Rã Retinex Một Giai Đoạn (One-stage Retinex)

### Công thức Retinex Cổ Điển
Lý thuyết Retinex truyền thống giả định một bức ảnh chụp $I$ là tích chập của hai thành phần:
$$I = R \odot L$$

Trong đó:
* $I$: Ảnh thiếu sáng đầu vào (đã quan sát được).
* $R$: Bản đồ phản xạ (**Reflectance** - đại diện cho cấu trúc bề mặt vật thể, không thay đổi theo ánh sáng). Đây chính là ảnh mục tiêu chúng ta cần khôi phục.
* $L$: Bản đồ ánh sáng (**Illumination** - đại diện cho sự phân bổ nguồn sáng trong không gian).
* $\odot$: Phép nhân ma trận từng pixel (element-wise multiplication).

---

### Công thức Retinex Cải Tiến Của Retinexformer
Trong môi trường thực tế, ảnh thiếu sáng luôn đi kèm với **nhiễu cảm biến nặng và lệch màu sắc**. Do đó, Retinexformer đề xuất bổ sung thêm một thành phần nhiễu $C$:
$$I = R \odot L + C$$

Tác giả thực hiện các bước biến đổi toán học thông minh như sau:
1. Trừ cả hai vế cho bản đồ ánh sáng $L$:
   $$I - L = R \odot L - L + C$$
2. Nhóm nhân tử chung $L$ ở vế phải:
   $$I - L = (R - \mathbf{1}) \odot L + C$$
3. Đặt $X = I - L$ (gọi là **Trạng thái thiếu sáng - Under-exposed Representation**). Đây chính là đầu vào được đưa vào chuỗi Transformer IGT để khôi phục:
   $$X = (R - \mathbf{1}) \odot L + C$$

> **Ý nghĩa vật lý**: 
> Công thức biến đổi này biến bài toán nhân phi tuyến phức tạp ($R \odot L$) thành một bài toán tìm kiếm tuyến tính tương đối ($X$). Lúc này, mạng nơ-ron Transformer chỉ cần học cách ước lượng sự sai lệch ánh sáng cục bộ để khôi phục ảnh $R$ sạch nhiễu một cách cực kỳ mượt mà.

---

## 🎯 2. Hệ Thống Các Hàm Loss Huấn Luyện (Loss Functions)

Để huấn luyện Retinexformer đạt chất lượng ảnh SOTA, tác giả sử dụng tổng hợp các hàm Loss đặc thù. Tổng hàm Loss của mô hình được định nghĩa như sau:

$$\mathcal{L}_{total} = \mathcal{L}_{rec} + \lambda_{perc} \mathcal{L}_{perc} + \lambda_{smooth} \mathcal{L}_{smooth}$$

*Trong đó, các hệ số $\lambda$ là trọng số để cân bằng tầm quan trọng của từng hàm Loss.*

### 2.1. Hàm Loss Tái Tạo (Reconstruction Loss - $\mathcal{L}_{rec}$)
Đo lường độ sai lệch trực tiếp ở cấp độ pixel giữa ảnh được tăng cường bởi mô hình ($I_{en}$) và ảnh sáng chuẩn Ground Truth ($I_{gt}$). Tác giả sử dụng **L1 Loss** (Mean Absolute Error) thay vì L2 Loss (MSE) vì L1 giúp bảo toàn độ sắc nét của các đường biên cạnh tốt hơn:

$$\mathcal{L}_{rec} = \frac{1}{N} \sum_{i=1}^{N} |I_{en}^{(i)} - I_{gt}^{(i)}|$$

---

### 2.2. Hàm Loss Cảm Nhận (Perceptual Loss - $\mathcal{L}_{perc}$)
* **Tại sao cần?** Đôi khi ảnh đầu ra có điểm số pixel rất sát với Ground Truth (L1 loss thấp) nhưng mắt người nhìn vào vẫn cảm thấy bị giả tạo hoặc bệt màu.
* **Cơ chế**: Tác giả nạp cả ảnh tăng sáng ($I_{en}$) và ảnh chuẩn ($I_{gt}$) vào một mạng nơ-ron tích chập đã được huấn luyện sẵn là **VGG-16** (được đóng băng trọng số). Hàm Loss cảm nhận sẽ tính toán khoảng cách Euclidean giữa các bản đồ đặc trưng (feature maps) ở các lớp sâu (lớp thứ $j$):

$$\mathcal{L}_{perc} = \sum_{j} \frac{1}{C_j H_j W_j} \|\Phi_j(I_{en}) - \Phi_j(I_{gt})\|_2^2$$

> **Ý nghĩa**: Ép mô hình khôi phục ảnh có ngữ nghĩa, cấu trúc và phong cách nghệ thuật tự nhiên nhất đối với cảm nhận thị giác của con người.

---

### 2.3. Hàm Loss Làm Mượt Bản Đồ Ánh Sáng (Illumination Smoothness Loss - $\mathcal{L}_{smooth}$)
Bản đồ ánh sáng trong tự nhiên thường biến thiên rất chậm và mịn màng ở các vùng phẳng, nhưng lại thay đổi đột ngột ở các khu vực biên cạnh của nguồn sáng. Hàm Loss này ép bản đồ ánh sáng ước lượng được ($L$) phải mịn màng về mặt không gian nhưng vẫn bảo toàn được các biên cạnh sắc nét bằng cách sử dụng các đạo hàm Gradient có trọng số:

$$\mathcal{L}_{smooth} = \sum_{x,y} \left( e^{-\alpha |\nabla_x R|} \cdot |\nabla_x L| + e^{-\alpha |\nabla_y R|} \cdot |\nabla_y L| \right)$$

*Trong đó $\nabla_x$ và $\nabla_y$ là đạo hàm theo chiều ngang và dọc, còn đạo hàm của Reflectance $R$ đóng vai trò là trọng số dẫn đường.*
