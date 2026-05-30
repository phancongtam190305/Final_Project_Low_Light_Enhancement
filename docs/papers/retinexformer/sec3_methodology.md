# Khảo Sát Chi Tiết Chương 3 (Methodology) - Retinexformer

Tài liệu này cung cấp một phân tích chuyên sâu và dễ hiểu về chương **3. Methodology (Phương pháp nghiên cứu)** của bài báo khoa học nổi tiếng: *"Retinexformer: One-stage Retinex-based Transformer for Low-Light Image Enhancement"* (ICCV 2023). Nội dung tập trung làm rõ bản chất toán học, cơ chế kiến trúc và tư duy thiết kế đột phá của nhóm tác giả nhằm giải quyết bài toán tăng cường ảnh thiếu sáng (LLIE).

---

## 1. Bối cảnh & Động lực (Context & Motivation)

### Thách thức của Tăng cường ảnh thiếu sáng (LLIE)
Trong điều kiện thiếu sáng, ảnh chụp thường gặp phải ba vấn đề nghiêm trọng đan xen:
1. **Độ tương phản cực thấp và mất chi tiết** ở các vùng tối sâu.
2. **Nhiễu hạt (noise) và vật thể giả (artifacts)** xuất hiện dày đặc do cảm biến phải đẩy ISO lên cao hoặc phơi sáng lâu.
3. **Méo màu (color distortion)** và hiện tượng thiếu/thừa sáng cục bộ sau khi cố gắng làm sáng ảnh bằng các thuật toán thông thường.

### Hạn chế của các phương pháp Retinex truyền thống và Deep Learning cũ
Lý thuyết Retinex cổ điển giả định một hình ảnh thiếu sáng $I$ có thể được phân rã thành hai thành phần độc lập: **Reflectance (Phản xạ bề mặt $R$)** và **Illumination (Bản đồ ánh sáng môi trường $L$**):
$$I = R \odot L$$
Tuy nhiên, mô hình này tồn tại hai điểm yếu chí mạng khi đưa vào thực tế:
* **Bỏ qua nhiễu vật lý:** Retinex cổ điển giả định ảnh đầu vào hoàn toàn sạch (corruption-free). Thực tế, khi ta làm sáng ảnh bằng cách chia cho bản đồ ánh sáng ($I \oslash L$), toàn bộ nhiễu hạt và lỗi cảm biến ẩn trong bóng tối sẽ bị khuếch đại lên gấp nhiều lần, tạo ra chất lượng ảnh rất tệ.
* **Quy trình đa giai đoạn (Multi-stage) cồng kềnh:** Các phương pháp Deep Learning dựa trên Retinex trước đây thường sử dụng các mạng CNN riêng biệt để thực hiện phân rã, khử nhiễu reflectance và tinh chỉnh bản đồ ánh sáng một cách độc lập. Sau đó, họ kết nối các mạng này lại để tinh chỉnh (fine-tune) đầu-cuối. Quy trình này rất tốn thời gian huấn luyện, phức tạp và dễ tích lũy sai số qua từng giai đoạn.

### Sự ra đời của Khung phân rã Retinex một giai đoạn cải tiến (ORF)
Để khắc phục triệt để các hạn chế trên, Retinexformer đề xuất **One-stage Retinex-based Framework (ORF)**. 

> [!NOTE]
> **Ý tưởng cốt lõi của ORF:** Thay vì coi ảnh thiếu sáng là sạch, ORF đưa trực tiếp các thành phần nhiễu/lỗi (perturbations) vào cả hai thành phần $R$ và $L$. Bằng các biến đổi toán học khéo léo (xem chi tiết ở phần 4), ORF chuyển đổi bài toán nhân bản đồ ánh sáng phức tạp thành bài toán phục hồi ảnh cộng tính đơn giản và ổn định:
> $$I_{lu} = R + C$$
> Trong đó, ảnh được làm sáng $I_{lu}$ chỉ bằng ảnh sạch mục tiêu $R$ cộng với một lượng nhiễu tổng hợp $C$. Lúc này, nhiệm vụ của mạng nơ-ron chỉ đơn giản là "khử nhiễu" $C$ khỏi ảnh $I_{lu}$ trong đúng **một giai đoạn duy nhất** được huấn luyện end-to-end.

### Tại sao Transformer kết hợp lý thuyết Retinex lại là "chìa khóa vàng"?
* **Hạn chế của CNN:** Mạng tích chập (CNN) xử lý ảnh dựa trên các bộ lọc cục bộ (local receptive field), dẫn đến việc khó nắm bắt mối tương quan toàn cục (long-range dependencies). Trong ảnh thiếu sáng, việc phục hồi một vùng tối sâu thường đòi hỏi thông tin ngữ cảnh và cấu trúc từ các vùng sáng tốt hơn ở rất xa.
* **Sức mạnh của Transformer:** Transformer với cơ chế tự chú ý (Self-Attention) toàn cục là giải pháp hoàn hảo để học các mối quan hệ xa này. Tuy nhiên, việc áp dụng Self-Attention trực tiếp lên ảnh độ phân giải cao sẽ ngốn một lượng tài nguyên cực lớn (độ phức tạp tính toán tăng theo cấp số nhân bậc hai của kích thước ảnh $\mathcal{O}(N^2)$).
* **Giải pháp Retinexformer:** Bằng cách sử dụng đặc trưng ánh sáng thu được từ lý thuyết Retinex làm **"hoa tiêu dẫn đường"** cho Transformer, mô hình có thể tập trung khả năng chú ý vào các vùng tối cần khử nhiễu sâu mà không bị quá tải thông tin. Đồng thời, cấu trúc tự chú ý được thiết kế lại theo chiều dọc (channel-wise) giúp giảm độ phức tạp tính toán xuống mức tuyến tính $\mathcal{O}(N)$, mở ra khả năng xử lý mượt mà trên mọi độ phân giải.

---

## 2. Vấn đề cốt lõi được giải quyết: Cơ chế IG-MSA

Khối **Illumination-Guided Multi-head Self-Attention (IG-MSA)** chính là trái tim và là đóng góp kỹ thuật lớn nhất của Retinexformer. 

### Cơ chế hoạt động chi tiết
Thông thường, cơ chế tự chú ý (Self-Attention) trong thị giác máy tính sẽ tính toán mối tương quan giữa mọi pixel này với mọi pixel khác trên không gian ảnh. Điều này cực kỳ tốn bộ nhớ VRAM. 

IG-MSA giải quyết triệt để bài toán này bằng cách chuyển đổi không gian chú ý: **tính toán sự chú ý giữa các kênh đặc trưng (channel-wise self-attention)** thay vì giữa các pixel không gian (spatial-wise). Mỗi bản đồ đặc trưng đơn kênh sẽ đóng vai trò là một "token".

Sự đột phá thực sự nằm ở việc **nhúng đặc trưng chiếu sáng (Light-up Feature $F_{lu}$)** trực tiếp vào công thức tính toán Self-Attention để điều tiết luồng thông tin:
1. Từ đặc trưng đầu vào $X$, mô hình tạo ra ba ma trận quen thuộc: **Query ($Q$)**, **Key ($K$)**, và **Value ($V$)**.
2. Đặc trưng chiếu sáng $F_{lu}$ (chứa thông tin về sự phân bổ ánh sáng và tương tác vùng sáng/tối do bộ ước lượng ORF cung cấp) được biến đổi thành ma trận dẫn đường **$Y$**.
3. Thay vì nhân trực tiếp ma trận chú ý với $V$ một cách mù quáng, IG-MSA thực hiện phép nhân từng phần tử (element-wise multiplication) giữa ma trận dẫn đường $Y$ và $V$:
   $$Attention = (Y \odot V) \cdot Softmax\left(\frac{K^T Q}{\alpha}\right)$$
   Điều này có nghĩa là **các đặc trưng giá trị ($V$) trước khi tham gia vào quá trình tổng hợp thông tin toàn cục sẽ được "nhúng qua một bộ lọc ánh sáng" $Y$**.

---

### Phép liên tưởng trực quan: "Chiếc kính lúp thông minh tích hợp đèn pin thích ứng"

Để hiểu một cách bình dân nhất về cách IG-MSA hoạt động, hãy tưởng tượng bạn là một **thám tử (mô hình AI)** đang bước vào một **căn phòng triển lãm tranh tối tranh sáng (bức ảnh thiếu sáng)** để khôi phục lại các bức tranh bị bám đầy bụi bặm và hư hại do thời gian (nhiễu hạt và lỗi cảm biến).

```
┌────────────────────────────────────────────────────────┐
│             CĂN PHÒNG TRANH TỐI TRANH SÁNG             │
│                                                        │
│  [Mảng tường sáng] ───────────────► [Góc khuất tối om]  │
│  (Chứa ngữ cảnh sạch)               (Dày đặc nhiễu hạt) │
└────────────────────────────────────────────────────────┘
                           ▲
                           │ (Dẫn đường chú ý)
            ┌──────────────┴──────────────┐
            │   KÍNH LÚP TÍCH HỢP ĐÈN PIN │  ◄── Đặc trưng ánh sáng (Flu)
            │      THÔNG MINH (IG-MSA)    │
            └─────────────────────────────┘
                           │ (Hành động)
                           ▼
┌────────────────────────────────────────────────────────┐
│  - Tự động soi sáng góc tối sâu.                      │
│  - Lấy thông tin cấu trúc từ mảng tường sáng đắp qua.   │
│  - Khử sạch nhiễu mà không làm cháy vùng sáng.        │
└────────────────────────────────────────────────────────┘
```

* **Nếu không có kính lúp dẫn đường (Self-Attention thông thường):** Bạn sẽ phải căng mắt nhìn với cùng một cự ly và cường độ lên tất cả mọi bức tranh trong phòng. Ở những bức tranh treo nơi quá tối, bạn chỉ nhìn thấy một màu đen kịt kèm theo các hạt bụi (nhiễu), còn ở những bức tranh treo dưới ánh đèn quá chói, bạn lại bị lóa mắt (over-exposure). Bạn tiêu tốn rất nhiều năng lượng (VRAM) nhưng hiệu quả thu được cực kỳ thấp vì không biết nên tập trung vào đâu.
* **Khi có chiếc kính lúp thông minh (IG-MSA):** Đặc trưng chiếu sáng $F_{lu}$ đóng vai trò y hệt chiếc **kính lúp tích hợp đèn pin thông minh** này:
  * **Tự động thích ứng:** Khi bạn rê kính vào những bức tranh ở góc khuất tối om, đèn pin tự động tăng cường độ sáng để soi rõ các nét vẽ ẩn sau lớp bụi. Kính ra lệnh cho não bộ của bạn: *"Hãy tập trung sự chú ý (Attention) vào đây để cạo sạch lớp bụi này!"*.
  * **Mượn ngữ cảnh khôi phục chi tiết:** Chiếc kính lúp nhận biết được cấu trúc nét vẽ ở mảng tường sáng đối diện rất đẹp và sạch sẽ. Nó gợi ý cho bạn sử dụng thông tin cấu trúc và tông màu từ mảng tường sáng đó để đắp vào, tái tạo lại bức tranh ở góc tối một cách hoàn hảo và tự nhiên nhất.
  * **Chống cháy sáng:** Khi rê kính qua vùng đã đủ sáng hoặc quá chói, đèn pin tự động dịu lại để tránh làm bức tranh bị cháy sáng hay bay màu.

Nhờ chiếc "kính lúp" IG-MSA này, Retinexformer không chỉ khử sạch nhiễu hạt ở các vùng tối sâu nhất mà còn bảo toàn nguyên vẹn độ sắc nét, màu sắc tự nhiên của toàn bộ bức ảnh mà không tiêu tốn tài nguyên vô ích.

---

## 3. Từ điển giải nghĩa thuật ngữ "khó hiểu"

Để giúp người đọc dễ dàng tiếp cận các tài liệu học thuật chuyên sâu, dưới đây là bảng giải nghĩa bình dân cho các khái niệm toán học và kỹ thuật xuất hiện trong chương này:

| Thuật ngữ | Định nghĩa học thuật | Giải nghĩa bình dân |
| :--- | :--- | :--- |
| **Query (Q)** | Ma trận truy vấn dùng để so khớp trong cơ chế Attention, biểu diễn câu hỏi của pixel hiện tại đối với các khu vực khác. | **"Câu hỏi tìm kiếm"** – Pixel tự hỏi: *"Tôi là một pixel vùng tối, tôi cần tìm những thông tin cấu trúc tương tự ở những đâu trong ảnh?"* |
| **Key (K)** | Ma trận khóa chứa các đặc trưng nhận dạng của tất cả các pixel, dùng để đối chiếu với Query. | **"Thẻ phân loại"** – Giống như các từ khóa index của các pixel khác để so khớp với câu hỏi của Query. |
| **Value (V)** | Ma trận chứa giá trị thông tin thực tế của các pixel, sẽ được tổng hợp dựa trên trọng số chú ý. | **"Nội dung thực tế"** – Khi Query và Key khớp nhau, mô hình sẽ lấy nội dung từ Value của các vùng đó để đắp vào vùng cần khôi phục. |
| **Softmax** | Hàm kích hoạt chuẩn hóa một vector các số thực thành một phân phối xác suất (tổng bằng 1). | **"Bộ chia tỷ lệ phần trăm"** – Giúp mô hình quyết định chính xác: *"Tôi nên dành 60% sự chú ý vào pixel A ở xa, 30% vào pixel B ở gần và 10% cho các vùng còn lại"*. |
| **Channel-wise** | Phép toán được thực hiện dọc theo chiều kênh đặc trưng (C) thay vì chiều không gian (H x W). | **"Xử lý theo chiều dọc"** – Thay vì quét qua từng pixel trên bức ảnh phẳng, ta xử lý các lớp đặc trưng xếp chồng lên nhau (giống như xử lý riêng biệt các tầng thông tin màu sắc và chi tiết ẩn). |
| **Element-wise ($\odot$)** | Phép toán (nhân, cộng, chia...) được thực hiện trực tiếp giữa các phần tử ở vị trí tương ứng của hai ma trận có cùng kích thước. | **"Nhân/Cộng đối ứng"** – Pixel ở hàng 1 cột 1 của ảnh này chỉ tương tác trực tiếp với đúng pixel ở hàng 1 cột 1 của ảnh kia, không liên quan đến xung quanh. |
| **VRAM** | Bộ nhớ truy cập ngẫu nhiên của card đồ họa (Video RAM), chuyên dùng để lưu trữ dữ liệu hình ảnh và trọng số mô hình khi tính toán. | **"Kho chứa của GPU"** – VRAM càng lớn thì mô hình càng chứa được nhiều đặc trưng và xử lý được ảnh độ phân giải càng cao mà không bị báo lỗi tràn bộ nhớ (Out of Memory). |
| **Độ phức tạp $\mathcal{O}(N)$ (Tuyến tính)** | Lượng tính toán tăng tỷ lệ thuận (tuyến tính) với kích thước dữ liệu đầu vào $N$. | **"Tăng đều ổn định"** – Nếu ảnh to gấp đôi, máy tính chỉ cần tốn gấp đôi thời gian và bộ nhớ để xử lý. Đây là mức cực kỳ tối ưu. |
| **Độ phức tạp $\mathcal{O}(N^2)$ (Bậc hai)** | Lượng tính toán tăng theo bình phương kích thước dữ liệu đầu vào $N$. | **"Tăng phi mã"** – Nếu ảnh to gấp đôi, máy tính phải tốn gấp **bốn** lần tài nguyên. Đây là lý do các Transformer truyền thống thường làm treo máy khi chạy ảnh lớn. |
| **Skip Connection** | Kỹ thuật kết nối tắt, truyền trực tiếp đặc trưng từ các tầng đầu sang các tầng cuối của mạng nơ-ron mà không qua các tầng trung gian. | **"Đường truyền tốc hành"** – Giúp giữ lại các chi tiết gốc nguyên bản của ảnh (như đường nét, góc cạnh) không bị mờ nhạt đi sau khi đi qua quá nhiều bộ lọc của mạng sâu. |

---

## 4. Hướng dẫn đọc hiểu công thức toán học và sơ đồ

Để đối chiếu trực tiếp với tệp PDF gốc của bài báo (*retinexformer.pdf*), bạn có thể theo dõi hướng dẫn từng bước dưới đây:

### Các phương trình toán học cốt lõi (Equations 1 to 6)

#### Phương trình (1): Mô hình Retinex cổ điển
$$I = R \odot L$$
* **Ý nghĩa:** Điểm xuất phát của lý thuyết. Một bức ảnh thiếu sáng $I$ được cấu thành bởi tích chập từng phần tử giữa Reflectance $R$ (phản xạ bề mặt vật thể - phần ta muốn khôi phục) và Illumination $L$ (ánh sáng môi trường).
* **Vấn đề:** Phương trình này không có chỗ cho nhiễu.

#### Phương trình (2): Mô hình Retinex một giai đoạn cải tiến (ORF)
$$I = (R + \hat{R}) \odot (L + \hat{L}) = R \odot L + R \odot \hat{L} + \hat{R} \odot (L + \hat{L})$$
* **Ý nghĩa:** Tác giả đưa thêm hai thành phần nhiễu vật lý: $\hat{R}$ (nhiễu hạt và chi tiết giả ẩn trong tối) và $\hat{L}$ (lỗi ước lượng ánh sáng gây méo màu/mất chi tiết). Phép khai triển toán học này giúp mô hình hóa toàn bộ các lỗi thực tế của ảnh thiếu sáng.

#### Phương trình (3): Biến đổi làm sáng thông minh
$$I \odot \bar{L} = R + R \odot (\hat{L} \odot \bar{L}) + (\hat{R} \odot (L + \hat{L})) \odot \bar{L}$$
* **Ý nghĩa:** Để làm sáng ảnh $I$, ta nhân cả 2 vế với bản đồ làm sáng $\bar{L}$ (thỏa mãn điều kiện lý tưởng $\bar{L} \odot L = 1$). Phép nhân này giúp cô lập được ảnh sạch mục tiêu $R$ ra một vế riêng biệt.

#### Phương trình (4): Công thức rút gọn thần kỳ
$$I_{lu} = I \odot \bar{L} = R + C$$
* **Ý nghĩa:** Đây là bước ngoặt toán học lớn nhất của bài báo! 
  * Tác giả gom toàn bộ các thành phần nhiễu phức tạp ở phương trình (3) thành một biến nhiễu tổng hợp duy nhất là **$C$** ($C = R \odot (\hat{L} \odot \bar{L}) + (\hat{R} \odot (L + \hat{L})) \odot \bar{L}$).
  * Bức ảnh được làm sáng $I_{lu}$ giờ đây chỉ đơn giản là bằng ảnh sạch $R$ cộng với nhiễu tổng hợp $C$. Bài toán nhân Retinex phức tạp đã được đưa về dạng toán **phục hồi ảnh cộng tính (additive restoration)** cực kỳ thân thiện với mạng nơ-ron Deep Learning.

#### Phương trình (5): Quy trình vận hành của ORF
$$(I_{lu}, F_{lu}) = \mathcal{E}(I, L_p), \quad I_{en} = \mathcal{R}(I_{lu}, F_{lu})$$
* **Ý nghĩa:** 
  * Bước 1: Bộ ước lượng ánh sáng $\mathcal{E}$ nhận ảnh đầu vào $I$ và bản đồ tiền nghiệm ánh sáng $L_p$ để tạo ra ảnh đã làm sáng $I_{lu}$ và đặc trưng chiếu sáng $F_{lu}$.
  * Bước 2: Bộ khôi phục $\mathcal{R}$ (chính là Transformer IGT) sử dụng đặc trưng hoa tiêu $F_{lu}$ để lọc bỏ toàn bộ nhiễu $C$ khỏi ảnh $I_{lu}$, trả về bức ảnh tăng cường hoàn hảo $I_{en}$.

#### Phương trình (6) & (7): Phân tách đa đầu chú ý (Multi-head Attention)
$$X = [X_1, X_2, \dots, X_k]$$
$$Q_i = X_i W_{Qi}^T, \quad K_i = X_i W_{Ki}^T, \quad V_i = X_i W_{Vi}^T$$
* **Ý nghĩa:** Đặc trưng đầu vào $X$ được chia thành $k$ phần (heads) đại diện cho các góc nhìn khác nhau. Mỗi phần được chiếu tuyến tính bằng các tham số học được để tạo ra các bộ ba $Q_i, K_i, V_i$ cho từng đầu tự chú ý.

#### Phương trình (9): Công thức tự chú ý dẫn đường bằng ánh sáng của IG-MSA
$$Attention(Q_i, K_i, V_i, Y_i) = (Y_i \odot V_i) \cdot Softmax\left(\frac{K_i^T Q_i}{\alpha_i}\right)$$
* **Ý nghĩa:** Trọng số chú ý được tính qua tích chập ma trận giữa Key và Query ($K_i^T Q_i$) và chuẩn hóa bằng hàm Softmax dưới sự điều tiết của tham số thích ứng $\alpha_i$. Sự khác biệt nằm ở chỗ ma trận đặc trưng Value $V_i$ được nhân trực tiếp với đặc trưng dẫn đường ánh sáng $Y_i$ (được phân tách từ $F_{lu}$). Điều này đảm bảo các vùng tối sâu được bảo vệ và xử lý khử nhiễu mạnh mẽ nhất nhờ sự dẫn đường của ánh sáng.

---

### Hướng dẫn đối chiếu Sơ đồ & Hình ảnh trong PDF gốc

#### Figure 2: Sơ đồ tổng quan kiến trúc Retinexformer (Trang 3 trong PDF)
Khi đọc sơ đồ này, bạn hãy chia làm 3 phần trực quan ứng với mô tả của tác giả:
1. **Nhánh (a) - Tổng quan luồng đi (Overview):**
   * Ở phía ngoài cùng bên trái, **Input Image** ($I$) và **Illumination Prior** ($L_p$) được đưa vào khối màu xanh lá cây nhạt **(i) Illumination Estimator**.
   * Bộ ước lượng này sinh ra **Light-up Feature** ($F_{lu}$) và **Light-up Map** ($\bar{L}$). Phép nhân chéo biểu thị việc làm sáng ảnh đầu vào tạo ra **Lit-up Image** ($I_{lu}$).
   * Cả $I_{lu}$ và $F_{lu}$ được truyền vào khối màu xanh dương **(ii) Corruption Restorer (IGT)** để tiến hành khử nhiễu và trả về **Enhanced Image** ($I_{en}$).
2. **Nhánh (b) - Khối xây dựng cơ bản (IGAB):**
   * Đây là cấu trúc chi tiết của một khối IGAB. Nó nhận đầu vào và đi qua lớp Chuẩn hóa (LN) đầu tiên, tiếp theo là khối **IG-MSA** (nơi nhúng đặc trưng ánh sáng $F_{lu}$), sau đó đi qua lớp LN thứ hai và khối Mạng truyền thẳng (FFN). Các đường mũi tên vòng biểu thị các kết nối tắt (Skip Connections).
3. **Nhánh (c) - Chi tiết cơ chế IG-MSA:**
   * Sơ đồ này vẽ chi tiết luồng xử lý toán học của phương trình (9). Bạn có thể thấy ma trận đặc trưng $X$ được biến đổi thành $Q, K, V$.
   * Đặc trưng chiếu sáng $F_{lu}$ được biến đổi thành ma trận dẫn đường $Y$.
   * Phép toán hình tròn có dấu chấm ở giữa biểu thị **phép nhân từng phần tử (element-wise) $Y \odot V$** trước khi nhân với ma trận chú ý đã qua hàm Softmax.

#### Figure 3: So sánh kết quả trực quan (Trang 5 trong PDF)
Hình ảnh này cung cấp cái nhìn thực tế về sức mạnh của Retinexformer so với các đối thủ SOTA khác trên hai tập dữ liệu chuẩn LOL-v1 (hàng trên) và LOL-v2 (hàng dưới):
* **Cách quan sát:** Hãy nhìn kỹ vào các vùng tối sâu trong các ô vuông được phóng to (zoomed-in patches).
* **Nhận diện lỗi của các phương pháp khác:**
  * Các phương pháp như *KinD*, *RUAS* thường làm xuất hiện các mảng màu giả, méo màu nghiêm trọng hoặc ảnh bị mờ nhòe, mất chi tiết cạnh.
  * Các phương pháp Transformer mạnh mẽ như *Restormer* vẫn để lại các đốm nhiễu hạt li ti ở các vùng quá tối do cơ chế tự chú ý chưa được định hướng tốt.
* **Sự vượt trội của Retinexformer:** Vùng tối được làm sáng lên cực kỳ tự nhiên, các chi tiết chữ viết hoặc hoa văn nhỏ được phục hồi sắc nét và đặc biệt là toàn bộ nhiễu hạt bị quét sạch hoàn toàn, mang lại màu sắc trung thực nhất so với ảnh gốc (Ground Truth).
