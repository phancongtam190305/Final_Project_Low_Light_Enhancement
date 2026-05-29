# Khảo Sát Nghiên Cứu & Hệ Thống Benchmarks - Nhánh 1: Paired Enhancement RGB

Tài liệu này tổng hợp và phân tích sâu các phương pháp tiêu biểu, hệ thống hóa kết quả benchmark định lượng trên tập dữ liệu chuẩn, đánh giá độ khó của các dataset và chỉ ra các khoảng trống nghiên cứu cốt lõi của Nhánh 1 (Tăng cường ảnh thiếu sáng có giám sát trên ảnh cặp RGB).

---
   
## 1. Bảng 1: Bảng So Sánh Các Phương Pháp Nền Tảng (Paper Methodology & Benchmarks)

Dưới đây là bảng so sánh chi tiết 5 mô hình tiêu biểu từ kinh điển đến SOTA hiện nay được áp dụng trong bài toán LLIE.

| Phương Pháp | Năm & Venue | Phân Loại Giám Sát | Ý Tưởng Cốt Lõi | PSNR (dB) / SSIM (LOL-v1) | Ưu Điểm | Nhược Điểm | Mã Nguồn (Code Link) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RetinexNet** | 2018 <br>BMVC | Học có giám sát (Supervised) | Kết hợp lý thuyết phân rã Retinex cổ điển với CNN sâu. Phân rã ảnh thành hai thành phần độc lập: **Reflectance** (Phản xạ bề mặt) và **Illumination** (Chiếu sáng), sau đó tăng sáng và khử nhiễu tách biệt. | 16.77 / 0.560 | - Tiên phong ứng dụng học sâu vào lý thuyết Retinex.<br>- Cấu trúc trực quan, dễ hiểu. | - Khử nhiễu kém, khuếch đại nhiễu nặng ở các vùng cực tối.<br>- Màu sắc đầu ra bị lệch, xuất hiện quầng sáng (halo artifacts). | [RetinexNet GitHub](https://github.com/weiqingyi/RetinexNet) |
| **Zero-DCE** | 2020 <br>CVPR | Học không giám sát / Không cặp ảnh (Zero-Reference) | Định nghĩa việc tăng sáng là bài toán ước lượng đường cong thích ứng ánh sáng vật lý (**Light-Enhancement Curve**). Sử dụng mạng nơ-ron tích chập siêu nhẹ để dự báo các hệ số của đường cong bậc cao thay vì ánh xạ pixel trực tiếp. | 17.10 / 0.558 | - Siêu nhẹ (79K params), tốc độ thời gian thực (>250 FPS).<br>- Không cần ảnh cặp (ground truth).<br>- Khả năng tổng quát hóa cực kỳ tốt. | - Do không giám sát bằng GT, mô hình không thể khử nhiễu cảm biến thực tế.<br>- Khôi phục chi tiết cấu trúc kém ở vùng tối sâu. | [Zero-DCE GitHub](https://github.com/Li-Chongyi/Zero-DCE) |
| **KinD (Kindling the Darkness)** | 2019 <br>ACM MM | Học có giám sát (Supervised) | Cải tiến mạnh mẽ từ RetinexNet. Thiết kế mạng phân rã linh hoạt và bổ sung thêm mô-đun khử nhiễu chuyên sâu (**Denoising module**) hoạt động trên không gian Reflectance và mô-đun điều chỉnh ánh sáng (**Illumination adjustment**). | 20.86 / 0.790 | - Khử nhiễu tốt hơn đáng kể so với RetinexNet.<br>- Cho phép người dùng tùy chỉnh độ sáng mong muốn linh hoạt.<br>- Ít bị lệch màu. | - Pipeline huấn luyện phức tạp, qua nhiều giai đoạn riêng lẻ (multi-stage training).<br>- Chi phí tính toán trung bình, có thể xuất hiện hiện tượng mờ ảnh (blurring). | [KinD GitHub](https://github.com/uqee/KinD) |
| **Restormer** | 2022 <br>CVPR | Học có giám sát (Supervised) | Kiến trúc Transformer hiệu năng cao thiết kế riêng cho phục hồi ảnh độ phân giải cao. Sử dụng cơ chế tự chú ý đa đầu theo chiều kênh (**MD-GSA**) và mạng cấp tiến tích hợp cổng (**GDFN**) để giảm tải tính toán. | 22.43 / 0.823 | - Khả năng khôi phục chi tiết bề mặt (texture) xuất sắc.<br>- Xử lý đa tác vụ phục hồi rất mạnh.<br>- Cực kỳ ổn định về cấu trúc hình học ảnh. | - Số lượng tham số rất lớn (~26M), yêu cầu bộ nhớ GPU cực cao khi training.<br>- Không được thiết kế chuyên biệt cho vật lý ánh sáng yếu (dễ cháy sáng nếu không có GT chuẩn). | [Restormer GitHub](https://github.com/swz30/Restormer) |
| **Retinexformer** | 2023 <br>ICCV | Học có giám sát (Supervised) | Mô hình SOTA kết hợp hoàn hảo lý thuyết Retinex một giai đoạn (**One-stage Retinex**) với Transformer. Sử dụng cơ chế tự chú ý dẫn đường bằng ánh sáng (**Illumination-Guided Attention - IGA**) để tập trung phục hồi vùng tối mà không làm cháy vùng sáng. | **25.16 / 0.845** | - Đạt điểm số PSNR/SSIM vượt trội trên LOL.<br>- Khử nhiễu tối ưu và giữ màu sắc tự nhiên một cách xuất sắc.<br>- Số lượng tham số tối ưu hơn nhiều so với Restormer. | - Độ phức tạp tính toán vẫn tương đối cao cho các thiết bị biên nhúng.<br>- Yêu cầu bộ dữ liệu paired chất lượng cao để đạt trạng thái tối ưu. | [Retinexformer GitHub](https://github.com/caiyuanhao1998/Retinexformer) |

---

## 2. Bảng 2: Bảng Chấm Điểm Độ Khó Dataset (Dataset Difficulty Ratings)

Thang điểm đánh giá từ **1 (Rất thấp / Rất dễ)** đến **5 (Cực kỳ cao / Cực kỳ khó)** đối với các tập dữ liệu Paired RGB:

| Dataset | Realism | Diversity | Difficulty | Ground Truth Quality | Benchmark Maturity | Reproducibility | Gap Potential | Tổng điểm trung bình |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **LOL (v1)** | 3/5 | 2/5 | 3/5 | 3/5 | 5/5 | 5/5 | 2/5 | **3.28** |
| **LOL-v2 (Real)** | 5/5 | 4/5 | 4/5 | 4/5 | 4/5 | 5/5 | 4/5 | **4.28** |
| **LOL-v2 (Syn)** | 2/5 | 4/5 | 3/5 | 5/5 | 4/5 | 5/5 | 3/5 | **3.71** |
| **SICE (Part 1/2)** | 5/5 | 5/5 | 5/5 | 4/5 | 3/5 | 4/5 | 5/5 | **4.43** |

### Giải thích chi tiết 7 tiêu chí đánh giá:
1. **Realism (Tính thực tế):** Đánh giá xem ảnh thiếu sáng có được chụp thực tế bằng thiết bị vật lý trong điều kiện tự nhiên hay không. LOL-v2 (Real) và SICE đạt điểm tối đa (5/5) do chụp hoàn toàn bằng máy DSLR, trong khi LOL-v2 (Syn) bị điểm thấp (2/5) vì chỉ mô phỏng toán học trên ảnh đủ sáng.
2. **Diversity (Độ đa dạng):** Đánh giá mức độ phong phú của bối cảnh (trong nhà, ngoài trời, xa, gần, ánh sáng đơn sắc/đa sắc). SICE dẫn đầu với sự đa dạng tuyệt đối về ngoại cảnh và kiến trúc. LOL (v1) bị điểm thấp (2/5) do chỉ chụp trong phòng tĩnh hẹp.
3. **Difficulty (Độ khó phục hồi):** Đánh giá mức độ phức tạp của nhiễu cảm biến, độ tối, sự phân bổ ánh sáng không đồng đều. SICE cực kỳ khó (5/5) vì có các vùng ngược sáng gắt và dải động cực rộng. LOL-v2 (Real) khó (4/5) do nhiễu hạt thực tế phân bố phức tạp.
4. **Ground Truth Quality (Chất lượng Ground Truth):** Đánh giá mức độ hoàn hảo, không nhiễu, không nhòe và căn chỉnh khớp chính xác pixel (pixel-wise) của ảnh tham chiếu. LOL-v2 (Syn) đạt 5/5 do khớp pixel tuyệt đối không sai lệch vật lý. SICE đạt 4/5 nhờ thuật toán fusion tối ưu nhưng có thể có bóng mờ nhẹ do dịch chuyển lá cây hoặc mây bay.
5. **Benchmark Maturity (Mức độ trưởng thành):** Đánh giá mức độ phổ biến trong cộng đồng học thuật và sự sẵn sàng của các baseline so sánh. LOL (v1) đạt điểm tuyệt đối (5/5) vì mọi bài báo LLIE đều bắt buộc phải so sánh trên dataset này.
6. **Reproducibility (Khả năng tái lập):** Đánh giá mức độ rõ ràng của protocol phân chia Train/Test và độ ổn định khi chạy lại mã nguồn. LOL và LOL-v2 rất dễ tái lập (5/5) vì có tập train/test chia sẵn rõ ràng. SICE khó hơn (4/5) do phân chia chuỗi và kích thước ảnh siêu lớn gây tốn bộ nhớ GPU.
7. **Gap Potential (Tiềm năng nghiên cứu):** Đánh giá khả năng khai thác các khoảng trống chưa được giải quyết trên dataset đó. SICE (5/5) và LOL-v2 (Real) (4/5) còn nhiều dư địa cải tiến chất lượng thị giác người dùng, trong khi LOL (v1) đã bão hòa (2/5) do các mô hình mới đã đạt trần chất lượng (PSNR >25 dB) và có xu hướng overfitting trên 15 ảnh test.

---

## 3. Phân Tích Chuyên Sâu 3 Khoảng Trống Nghiên Cứu (Research Gaps)

Mặc dù Nhánh 1 (Paired Enhancement RGB) đã đạt được những bước tiến vượt bậc với các kiến trúc Transformer SOTA, nhưng thực tế nghiên cứu vẫn đối mặt với 3 nút thắt cổ chai lớn sau:

### 🔴 Khoảng trống 1: Sự phụ thuộc nghiêm trọng vào dữ liệu cặp và Sự sụp đổ năng lực tổng quát hóa (Domain Shift & Generalization Collapse)
* **Bản chất vấn đề:** Các mô hình học có giám sát dựa trên ảnh cặp (như Retinexformer hay Restormer) học cách ánh xạ phân phối pixel tối sang phân phối pixel sáng cụ thể của tập dữ liệu huấn luyện. Do LOL hay LOL-v2 được chụp trong những bối cảnh phòng Lab hoặc phố đêm giới hạn với một vài dòng máy DSLR cố định, mô hình sẽ bị "overfitting" vào đặc trưng phân phối quang học của cảm biến đó.
* **Hậu quả thực tế:** Khi đem các mô hình SOTA này chạy thử nghiệm trực tiếp trên ảnh chụp thiếu sáng từ camera điện thoại thông minh (iPhone, Samsung) hoặc camera an ninh (IP Camera) ngoài đường phố thực tế, chất lượng phục hồi bị suy giảm nghiêm trọng. Ảnh xuất hiện các quầng màu giả tạo (color cast), nhiễu hạt bị phóng đại thành các đốm màu loang lổ, và độ tương phản trông cực kỳ thiếu tự nhiên.
* **Hướng giải quyết tiềm năng:** Cần nghiên cứu các phương pháp thích ứng miền (Domain Adaptation), học tự giám sát (Self-Supervised) kết hợp huấn luyện đa miền (Multi-domain training) để phá vỡ sự lệ thuộc vào phân phối ảnh cặp hẹp.

### 🔴 Khoảng trống 2: Sai lệch căn chỉnh pixel vật lý và Hiện tượng tạo tác giả tạo (Pixel Misalignment & Fake Artifacts)
* **Bản chất vấn đề:** Việc thu thập một cặp ảnh phơi sáng ngắn (tối) và phơi sáng dài (sáng) trong thế giới thực luôn phải đối mặt với sai lệch hình học cơ học. Dù máy ảnh được đặt trên chân đế tripod chuyên dụng, thao tác bấm máy cơ học, gió nhẹ, hoặc sự chuyển động vi mô của không khí vẫn gây ra sự lệch dịch chuyển pixel (sub-pixel shift) giữa hai bức ảnh.
* **Hậu quả thực tế:** Các hàm tổn thất truyền thống (như L1 Loss, L2 Loss) hoạt động dựa trên việc so sánh trực tiếp từng pixel tương ứng ($pixel-to-pixel$). Khi dữ liệu cặp bị lệch dù chỉ 1-2 pixel, mô hình sẽ bị "bối rối" trong quá trình tối ưu hóa. Kết quả là mô hình có xu hướng làm mờ (blurring) các cạnh sắc nét, tạo ra các bóng mờ (ghosting) hoặc quầng sáng giả (halo artifacts) bao quanh các cấu trúc viền vật thể nhằm cực tiểu hóa lỗi trung bình bình phương (MSE).
* **Hướng giải quyết tiềm năng:** Thiết kế các hàm loss bất biến với dịch chuyển (alignment-invariant losses) như Perceptual Loss cải tiến, Contextual Loss hoặc tích hợp các mạng con tự động căn chỉnh (Coarse-to-fine alignment networks) trước khi đưa vào mạng tăng cường.

### 🔴 Khoảng trống 3: Sự xung đột giữa khôi phục độ sáng và Phóng đại nhiễu cảm biến (Illumination Restoration vs. Noise Amplification)
* **Bản chất vấn đề:** Trong điều kiện ánh sáng cực tối, tỷ số tín hiệu trên nhiễu (Signal-to-Noise Ratio - SNR) của cảm biến ảnh giảm xuống gần mức tối thiểu. Các pixel tối không chỉ chứa thông tin ánh sáng yếu mà còn bị trộn lẫn với các thành phần nhiễu vật lý phức tạp (Read noise, Shot noise). 
* **Hậu quả thực tế:** Quá trình tăng cường độ sáng thực chất là một phép nhân tuyến tính hoặc phi tuyến cường độ pixel. Khi mô hình nâng độ sáng lên gấp 10-20 lần để đạt mức Ground Truth, các hạt nhiễu ẩn sâu trong vùng tối cũng bị phóng đại lên gấp bấy nhiêu lần. Các mô hình paired RGB thường rơi vào hai thái cực cực đoan:
  1. *Khử nhiễu quá đà (Over-smoothing):* Làm mất hoàn toàn các chi tiết vân bề mặt hạt mịn (textures), khiến ảnh trông bết bát như tranh vẽ sáp màu.
  2. *Khử nhiễu không sạch (Under-denoising):* Để lại các vệt nhiễu màu (chroma noise) loang lổ dạng tím/xanh lá cực kỳ mất thẩm mỹ trên các mảng tường phẳng tối.
* **Hướng giải quyết tiềm năng:** Nghiên cứu cấu trúc tích hợp phân tách tần số (Frequency-domain learning like Wavelet or Fourier Transform) để xử lý nhiễu ở tần số cao độc lập với việc khôi phục cấu trúc ánh sáng ở tần số thấp.
