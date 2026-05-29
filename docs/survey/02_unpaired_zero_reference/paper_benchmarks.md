# Khảo Sát Nghiên Cứu & Hệ Thống Benchmarks - Nhánh 2: Unpaired / Zero-Reference

Tài liệu này tổng hợp và phân tích sâu các phương pháp tiêu biểu, hệ thống hóa kết quả benchmark phi tham chiếu trên các tập dữ liệu thực tế, đánh giá độ khó của các dataset và chỉ ra các khoảng trống nghiên cứu cốt lõi của Nhánh 2 (Tăng cường ảnh thiếu sáng không giám sát, học không cần cặp ảnh hoặc Zero-Shot).

---

## 1. Bảng 1: Bảng So Sánh Các Phương Pháp Nền Tảng (Paper Methodology & Benchmarks)

Dưới đây là bảng so sánh 5 mô hình tiêu biểu được áp dụng để đánh giá trên các tập dữ liệu Unpaired thực tế (DICM, LIME, MEF, NPE) thông qua chỉ số **NIQE** (Naturalness Image Quality Evaluator - *càng thấp càng tốt / trông càng tự nhiên*).

| Phương Pháp | Năm & Venue | Phân Loại Giám Sát | Ý Tưởng Cốt Lõi | Chỉ số NIQE tiêu biểu (DICM / LIME / NPE) | Ưu Điểm | Nhược Điểm | Mã Nguồn (Code Link) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RetinexNet** | 2018 <br>BMVC | Học có giám sát (Supervised) | Phân rã ảnh thành Reflectance và Illumination dưới dạng giám sát cặp. Dùng để test khả năng tổng quát hóa ngoại miền. | ~4.33 / ~5.75 / ~4.95 | - Khả năng kéo sáng vùng tối rất tốt do được học từ dữ liệu cặp LOL. | - Bị lệch màu nặng nề và khuếch đại nhiễu cực đoan khi đem sang ảnh thực tế.<br>- Điểm NIQE tương đối cao (thiếu tự nhiên). | [RetinexNet GitHub](https://github.com/weiqingyi/RetinexNet) |
| **Zero-DCE** | 2020 <br>CVPR | Học không giám sát / Không cặp ảnh (Zero-Reference) | Ước lượng các đường cong điều chỉnh ánh sáng phi tuyến tính cục bộ thông qua tập hợp các hàm loss phi tham chiếu (Spatial Consistency, Exposure Control, Color Constancy). | ~4.58 / ~5.82 / ~4.53 | - Huấn luyện cực kỳ nhanh, mô hình siêu nhẹ.<br>- Không cần ảnh Ground Truth.<br>- Cực kỳ bền bỉ, không bao giờ bị méo dạng hình học ảnh. | - Hoàn toàn không thể khử nhiễu cảm biến do thiết kế loss không hỗ trợ.<br>- Dễ bị cháy sáng nhẹ ở các vùng phơi sáng sẵn nếu không tinh chỉnh tham số. | [Zero-DCE GitHub](https://github.com/Li-Chongyi/Zero-DCE) |
| **KinD (Kindling the Darkness)** | 2019 <br>ACM MM | Học có giám sát (Supervised) | Thiết kế mạng phân rã ba thành phần linh hoạt, tối ưu hóa riêng biệt cấu trúc chiếu sáng và khử nhiễu cảm biến chuyên sâu. | **~3.95 / ~4.42 / ~3.92** | - Khử nhiễu xuất sắc trên các ảnh unpaired thực tế.<br>- Bảo toàn cấu trúc viền tốt.<br>- Điểm NIQE cực kỳ tối ưu. | - Kiến trúc tương đối nặng và quy trình huấn luyện nhiều giai đoạn phức tạp.<br>- Phụ thuộc vào chất lượng tiền huấn luyện trên LOL. | [KinD GitHub](https://github.com/uqee/KinD) |
| **Restormer** | 2022 <br>CVPR | Học có giám sát (Supervised) | Transformer hiệu năng cao phục hồi chi tiết pixel. Được dùng làm baseline so sánh khả năng thích ứng miền khi chạy suy diễn trực tiếp trên ảnh thực tế. | ~3.80 / ~4.30 / ~3.85 | - Khôi phục cấu trúc vân bề mặt (texture) sắc nét ấn tượng.<br>- Hạn chế tối đa hiện tượng mờ nhòe (blur). | - Tiêu tốn cực kỳ nhiều tài nguyên phần cứng.<br>- Dễ xuất hiện hiện tượng đổi màu lạ (color artifact) tại các vùng ngược sáng gắt. | [Restormer GitHub](https://github.com/swz30/Restormer) |
| **Retinexformer** | 2023 <br>ICCV | Học có giám sát (Supervised) | Sử dụng Illumination-Guided Attention (IGA) để điều phối năng lực tính toán của Transformer tập trung vào các vùng tối thiếu sáng. | **~3.65 / ~4.10 / ~3.70** | - Khôi phục màu sắc tự nhiên và chân thực vượt trội.<br>- Khử nhiễu biên rất sạch mà không làm bết ảnh.<br>- Đạt chỉ số NIQE ở mức SOTA hiện nay. | - Đòi hỏi năng lực tính toán cao.<br>- Vẫn có thể bị quầng sáng (halo effect) nhẹ ở ranh giới giữa vùng siêu tối và siêu sáng. | [Retinexformer GitHub](https://github.com/caiyuanhao1998/Retinexformer) |

---

## 2. Bảng 2: Bảng Chấm Điểm Độ Khó Dataset (Dataset Difficulty Ratings)

Thang điểm đánh giá từ **1 (Rất thấp / Rất dễ)** đến **5 (Cực kỳ cao / Cực kỳ khó)** đối với các tập dữ liệu Unpaired:

| Dataset | Realism | Diversity | Difficulty | Ground Truth Quality | Benchmark Maturity | Reproducibility | Gap Potential | Tổng điểm trung bình |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DICM (69 ảnh)** | 5/5 | 5/5 | 3/5 | **1/5** | 5/5 | 5/5 | 3/5 | **3.86** |
| **LIME (10 ảnh)** | 5/5 | 3/5 | 4/5 | **1/5** | 5/5 | 5/5 | 3/5 | **3.71** |
| **MEF (17 ảnh)** | 5/5 | 4/5 | 4/5 | **1/5** | 4/5 | 5/5 | 4/5 | **4.00** |
| **NPE (85 ảnh)** | 5/5 | 5/5 | 5/5 | **1/5** | 5/5 | 5/5 | 5/5 | **4 .43** |

### Giải thích chi tiết 7 tiêu chí đánh giá cho Unpaired Datasets:
1. **Realism (Tính thực tế):** Đạt điểm tuyệt đối (5/5) ở cả 4 dataset do dữ liệu hoàn toàn là ảnh chụp đời thực bằng các thiết bị máy ảnh thương mại cầm tay trong bối cảnh tự nhiên, không qua bất kỳ quy trình giả lập toán học nào.
2. **Diversity (Độ đa dạng):** DICM và NPE đạt 5/5 nhờ tập hợp bối cảnh phong phú (đường phố, phong cảnh, vật thể động, con người, nội thất). LIME thấp hơn (3/5) vì quy mô quá nhỏ (10 ảnh) và chủ yếu là cảnh phố đêm tĩnh.
3. **Difficulty (Độ khó phục hồi):** NPE khó nhất (5/5) do phân bổ ánh sáng cực kỳ không đồng đều (**non-uniform illumination**), nhiều vùng ngược sáng và bóng râm sâu. LIME và MEF khó (4/5) do độ tối rất sâu và dải động phức tạp. DICM ở mức trung bình (3/5) vì ảnh thiếu sáng ở mức độ phơi sáng vừa phải, dễ kéo sáng hơn.
4. **Ground Truth Quality (Chất lượng Ground Truth):** Đạt điểm tối thiểu **1/5** cho cả 4 dataset vì đây là tập dữ liệu **Unpaired**, hoàn toàn không chứa bất kỳ ảnh Ground Truth hay ảnh tham chiếu nào. Việc phục hồi hoàn toàn dựa vào tính tự nhiên nội tại của ảnh.
5. **Benchmark Maturity (Mức độ trưởng thành):** Rất cao (5/5) do cả 4 dataset đều là những tiêu chuẩn bắt buộc phải sử dụng để đánh giá năng lực tổng quát hóa trong mọi bài báo khoa học về LLIE từ năm 2016 đến nay.
6. **Reproducibility (Khả năng tái lập):** Tuyệt đối (5/5) do dung lượng cực nhẹ (chỉ từ 10 đến 85 ảnh), chạy suy diễn (inference) chỉ mất vài giây đến vài chục giây, không cần quy trình huấn luyện hay phân chia phức tạp.
7. **Gap Potential (Tiềm năng nghiên cứu):** NPE (5/5) và MEF (4/5) còn rất nhiều tiềm năng khai phá, đặc biệt trong việc nghiên cứu các cơ chế tự thích ứng phơi sáng cục bộ (local exposure adjustment) và bảo toàn tính tự nhiên của màu sắc dưới ánh sáng phức tạp.

---

## 3. Phân Tích Chuyên Sâu 3 Khoảng Trúng Nghiên Cứu (Research Gaps)

Nhánh 2 (Unpaired / Zero-Reference) mặc dù giải quyết triệt để sự phụ thuộc vào ảnh cặp và có tốc độ suy diễn vượt trội, nhưng vẫn đối mặt với 3 bài toán nan giải chưa có lời giải hoàn hảo:

### 🔴 Khoảng trống 1: Sự mơ hồ của các Metric phi tham chiếu và Hiện tượng "Ảo ảnh thẩm mỹ" (Metric Ambiguity & Visual Hallucination)
* **Bản chất vấn đề:** Do hoàn toàn không có ảnh Ground Truth để tính toán PSNR/SSIM, các mô hình Unpaired phải dựa vào các chỉ số đánh giá không tham chiếu như **NIQE** hoặc **BRISQUE**. Tuy nhiên, NIQE được xây dựng dựa trên việc đo đạc sự sai lệch thống kê phân phối tự nhiên của ảnh sạch, chứ không đo đạc độ chính xác về thông tin ngữ nghĩa (semantic correctness).
* **Hậu quả thực tế:** Một mô hình tăng cường ảnh có thể cố tình làm mịn ảnh cực mạnh (over-smoothing) để triệt tiêu toàn bộ nhiễu, làm mất sạch các chi tiết nhỏ sắc nét nhưng lại đạt được điểm NIQE cực kỳ tốt (thấp) do ảnh không còn các hạt nhiễu gây sai lệch thống kê. Ngược lại, một bức ảnh được tăng sáng xuất sắc, giữ nguyên từng sợi tóc hay vân gỗ nhưng còn sót lại một chút nhiễu cảm biến tự nhiên lại bị điểm NIQE rất tệ. Điều này dẫn đến sự mâu thuẫn lớn giữa đánh giá định lượng toán học và cảm nhận thị giác thực tế của con người. Ngoài ra, các mạng GAN (như EnlightenGAN) không có GT ràng buộc pixel thường tự sinh ra các chi tiết giả tạo (hallucination artifacts) tại các vùng quá tối.
* **Hướng giải quyết tiềm năng:** Nghiên cứu và xây dựng các hệ đo lường mới dựa trên Mô hình Đa phương thức Lớn (LMMs like GPT-4o, LLaVA) hoặc CLIP-based Image Quality Assessment (CLIP-IQA) để đánh giá độ thẩm mỹ và tính chân thực tiệm cận mắt người nhất.

### 🔴 Khoảng trống 2: Sự bất lực trong kiểm soát nguồn sáng điểm cục bộ và Hiện tượng cháy sáng gắt (Artificial Light Source Control & Extreme Over-exposure)
* **Bản chất vấn đề:** Các thuật toán Zero-Reference (như Zero-DCE) huấn luyện dựa trên hàm tổn thất Kiểm soát Phơi sáng (**Exposure Control Loss**), cố gắng ép giá trị trung bình của các vùng không gian ảnh về một mức xám lý tưởng (thường là $0.6$). Loss này hoạt động hiệu quả khi toàn cảnh tối đều. Nhưng đối với ảnh phố đêm thực tế chứa các nguồn sáng điểm nhân tạo cực mạnh (bóng đèn đường, bảng hiệu LED, đèn pha ô tô) nằm xen kẽ giữa các ngõ tối sâu, mô hình sẽ bị mất phương hướng.
* **Hậu quả thực tế:** Do không có Ground Truth định hướng giới hạn phơi sáng cho từng pixel cụ thể, mô hình khi cố gắng kéo sáng các ngõ tối sẽ vô tình nâng cường độ của các nguồn sáng điểm vốn đã sáng sẵn lên mức cực đại. Kết quả là các bảng hiệu LED bị cháy trắng hoàn toàn, mất sạch thông tin chữ, các bóng đèn đường bị loang lổ quầng sáng giả (halo artifacts) che lấp toàn bộ chi tiết xung quanh.
* **Hướng giải quyết tiềm năng:** Tích hợp các bản đồ phân vùng chú ý nguồn sáng (Saliency maps hoặc Light-source attention masks) vào hàm loss để khống chế dải động phơi sáng một cách phi tuyến tính và cục bộ.

### 🔴 Khoảng trống 3: Sự bất lực hoàn toàn trước Nhiễu cảm biến sâu và Hiện tượng loang lổ màu (Inability to Handle Deep Sensor Noise & Color Casts)
* **Bản chất vấn đề:** Trong chụp ảnh ánh sáng yếu thực tế, bóng tối luôn đi đôi với nhiễu cảm biến cực nặng (shot noise, read noise). Tuy nhiên, các hàm loss phi tham chiếu vật lý của nhánh Zero-Reference chỉ có thể tối ưu hóa độ tương phản, màu sắc và độ phơi sáng, chứ **hoàn toàn không thể tự phân biệt được đâu là chi tiết ảnh thật và đâu là hạt nhiễu cảm biến** để tiến hành loại bỏ nếu không có sự định hướng từ Ground Truth sạch.
* **Hậu quả thực tế:** Khi Zero-DCE hoặc các biến thể của nó nâng độ sáng của ảnh lên, chúng vô tình nâng cả biên độ của các hạt nhiễu ẩn sâu trong bóng tối lên gấp nhiều lần. Ảnh đầu ra mặc dù rất sáng và rõ nét nhưng lại bị phủ một lớp nhiễu hạt khổng lồ, loang lổ các đốm màu xanh đỏ (chroma noise) cực kỳ mất thẩm mỹ. Ngay cả các mô hình GAN cố gắng khử nhiễu bằng Discriminator cũng thường làm bệt màu ảnh hoặc tạo ra các vân nhiễu dạng sóng lạ mắt.
* **Hướng giải quyết tiềm năng:** Phát triển các kiến trúc lai song song (Hybrid architectures) kết hợp mạng ước lượng ánh sáng không giám sát với một mạng khử nhiễu tự giám sát (Self-supervised denoising like Noise2Noise or Neighbor2Neighbor) để xử lý đồng thời hai tác vụ tăng sáng và lọc nhiễu mà không cần dữ liệu cặp.
