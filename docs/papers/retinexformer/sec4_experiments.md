# Phân Tích Chuyên Sâu Chương 4: Thực Nghiệm (Experiments) - Retinexformer

Tài liệu này cung cấp một bản phân tích chi tiết, dễ hiểu và chuẩn mực học thuật bằng Tiếng Việt về **Chương 4 (Experiments)** của bài báo khoa học *Retinexformer: One-stage Retinex-based Transformer for Low-Light Image Enhancement* (CVPR 2023). Bản hướng dẫn này được thiết kế đặc biệt nhằm giúp học viên cao học hoặc sinh viên làm đồ án tốt nghiệp dễ dàng tiếp cận, nắm bắt số liệu thực nghiệm mà không bị ngợp bởi các bảng biểu và thuật ngữ chuyên ngành phức tạp.

---

## 1. Bối cảnh & Động lực (Context & Motivation)

### Tại sao chương thực nghiệm này tồn tại?
Trong nghiên cứu khoa học máy tính nói chung và lĩnh vực Tăng cường ảnh thiếu sáng (Low-Light Image Enhancement - LLIE) nói riêng, một đề xuất lý thuyết mới dù có hay và logic đến đâu (như khung ORF sửa đổi mô hình Retinex truyền thống hay cơ chế tự chú ý IG-MSA) vẫn chỉ dừng lại ở mức **giả thuyết** cho đến khi nó được kiểm chứng thực tế. 

Chương thực nghiệm tồn tại nhằm mục đích:
1. **Kiểm chứng khoa học (Scientific Verification):** Chứng minh bằng số liệu định lượng (Quantitative) và kết quả trực quan (Qualitative) rằng Retinexformer thực sự vượt trội hơn các công nghệ hiện tại (State-Of-The-Art - SOTA).
2. **Đánh giá hiệu năng đa chiều (Multi-dimensional Evaluation):** Thử nghiệm mô hình trên nhiều kịch bản dữ liệu khác nhau (ảnh nén RGB, ảnh RAW phơi sáng cực ngắn, video trong nhà và ngoài trời) để đo lường khả năng tổng quát hóa (generalization).
3. **Đo lường tính thực tiễn (Practical Utility):** Chứng minh rằng ảnh sau khi được làm sáng bằng Retinexformer không chỉ "đẹp mắt người" mà còn giúp ích cho các tác vụ thị giác máy tính bậc cao hơn (như phát hiện vật thể - Object Detection).
4. **Chứng minh tính kinh tế (Computational Efficiency):** Transformer nổi tiếng là "ngốn phần cứng". Thực nghiệm này phải chỉ ra rằng Retinexformer vừa mạnh mẽ vừa nhẹ nhàng, tiết kiệm tài nguyên tính toán (dung lượng bộ nhớ, thời gian xử lý).

> [!NOTE]
> **Động lực cốt lõi:** Tác giả muốn khẳng định Retinexformer đã giải quyết triệt để hai điểm nghẽn lớn của các nghiên cứu trước đó: (1) hiện tượng khuếch đại nhiễu và sai lệch màu sắc của các phương pháp Retinex cũ, và (2) chi phí tính toán cực kỳ đắt đỏ (độ phức tạp bình phương) của các kiến trúc Transformer truyền thống.

---

## 2. Vấn đề cốt lõi được giải quyết (Core Problem)
*Hướng dẫn đọc hiểu hệ thống bảng số liệu phức tạp trong bài báo để không bị ngợp.*

Khi mới tiếp cận bài báo Retinexformer, người học rất dễ bị choáng ngợp bởi hàng loạt bảng biểu chứa hàng trăm con số. Dưới đây là chiếc "la bàn" giúp bạn giải mã từng bảng một cách khoa học:

### 2.1. Bảng so sánh hiệu năng tổng thể: Table 1 & Table 2 (Quantitative Results)
Hai bảng này đại diện cho cuộc đối đầu trực tiếp giữa Retinexformer và **15 phương pháp SOTA khác** (bao gồm các mô hình CNN truyền thống, mô hình dựa trên lý thuyết Retinex sâu, và các Transformer phục hồi ảnh mạnh mẽ như Restormer, Uformer, IPT).

#### Cách đọc Table 1 (Trang 6 trong PDF):
*   **Các cột dọc đại diện cho 7 bộ dữ liệu chuẩn (Benchmarks):**
    *   `LOL-v1` và `LOL-v2-real` / `LOL-v2-syn`: Bộ dữ liệu ảnh thiếu sáng thực tế và tổng hợp cực kỳ phổ biến.
    *   `SID` và `SMID`: Bộ dữ liệu chụp cảnh cực tối ở định dạng RAW (sau đó chuyển sang RGB). Đây là thuốc thử cực mạnh vì ảnh gốc bị nhiễu vô cùng nặng.
    *   `SDSD-in` (indoor) và `SDSD-out` (outdoor): Bộ dữ liệu video tĩnh thiếu sáng trong nhà và ngoài trời.
*   **Các dòng ngang:** Danh sách các phương pháp đối thủ.
*   **Các chỉ số đánh giá cốt lõi tại mỗi cột:** Cặp chỉ số **PSNR** (càng cao càng tốt) và **SSIM** (càng gần 1 càng tốt).
*   **Cột độ phức tạp tính toán (Complexity):** 
    *   `Params (M)` (Triệu tham số - càng nhỏ càng nhẹ).
    *   `FLOPs (G)` (Tỷ phép tính dấu phẩy động - càng nhỏ càng chạy nhanh).
*   **Quy ước màu sắc của tác giả:**
    *   Số in **màu đỏ**: Kết quả tốt nhất (Hạng 1).
    *   Số in **màu xanh dương**: Kết quả tốt nhì (Hạng 2).

> [!TIP]
> **Thông điệp cốt lõi từ Table 1:** Bạn hãy nhìn vào dòng cuối cùng (`Retinexformer`). Bạn sẽ thấy một sắc đỏ bao phủ hầu hết các cột chỉ số PSNR/SSIM. Retinexformer vượt trội hơn tất cả các đối thủ lớn. Đặc biệt, so với đối thủ nặng ký nhất là **SNR-Net**, Retinexformer cải thiện PSNR từ **0.33 dB đến 1.57 dB** trên khắp các bộ dữ liệu, trong khi chỉ tiêu tốn **40% số lượng tham số** (1.61M so với 4.01M) và **59% năng lượng tính toán** (15.57G FLOPS so với 26.35G FLOPS).

#### Cách đọc Table 2 (Trang 6 trong PDF):
*   Bảng này so sánh riêng trên bộ dữ liệu **MIT-Adobe FiveK** danh tiếng (sử dụng ảnh được chỉnh sửa bởi chuyên gia C làm Ground Truth).
*   Kết quả cho thấy Retinexformer đạt **PSNR cao nhất (24.94 dB)** vượt qua Restormer (24.13 dB) và SNR-Net (23.81 dB) nhưng với chi phí tính toán FLOPS nhỏ hơn Restormer gấp gần 10 lần (15.57G so với 144.3G).

---

### 2.2. Đánh giá tính thực tiễn và nhận thức: Table 3 (User Study & Object Detection)
Tác giả không chỉ dừng lại ở các chỉ số toán học khô khan (PSNR/SSIM) mà còn chứng minh giá trị thực tế qua hai bài kiểm tra quan trọng:

#### Table 3a: Thử nghiệm đánh giá từ người dùng (User Study Scores)
*   **Bối cảnh:** Thuật toán tăng cường ảnh đôi khi đạt điểm PSNR rất cao nhưng ảnh trông rất giả tạo hoặc khó chịu đối với mắt người. Tác giả đã mời **23 người thử nghiệm độc lập** để đánh giá trực quan **156 bức ảnh** sau khi tăng cường (được ẩn danh tên phương pháp để đảm bảo khách quan).
*   **Thang điểm:** Từ 1 (tệ nhất) đến 5 (đẹp nhất) dựa trên 3 tiêu chí: (i) không bị cháy sáng/tối, (ii) không bị lệch màu, (iii) sạch nhiễu/artifacts.
*   **Kết quả:** Retinexformer đạt điểm trung bình cao nhất (**3.77**), đứng đầu trên 5 bộ dữ liệu và đứng thứ hai trên 2 bộ dữ liệu còn lại. Điều này chứng minh thuật toán của tác giả rất hợp nhãn quan sinh học của con người.

#### Table 3b: Tác vụ phát hiện vật thể thiếu sáng trên bộ dữ liệu ExDark
*   **Bối cảnh:** Trong xe tự lái hoặc camera an ninh ban đêm, tăng cường ảnh là bước đệm (preprocessing) cho các hệ thống AI nhận diện vật thể. Tác giả sử dụng mô hình phát hiện vật thể **YOLO-v3** (huấn luyện từ đầu) trên bộ dữ liệu ảnh thiếu sáng **ExDark** (gồm 12 loại vật thể như xe hơi, thuyền, mèo, chó...).
*   **Chỉ số:** **AP (Average Precision - Độ chính xác trung bình)** trên từng loại vật thể và **mAP (Mean AP - Trung bình toàn bộ)**.
*   **Kết quả:** Ảnh được xử lý bởi Retinexformer giúp YOLO-v3 đạt **mAP cao nhất (66.1%)**, vượt trội hơn tất cả các phương pháp tiền xử lý khác. Điều này chứng minh Retinexformer bảo toàn cực tốt các đặc trưng ngữ nghĩa (shapes, edges) cần thiết cho AI bậc cao.

---

### 2.3. Bóc tách từng mảnh ghép công nghệ: Table 4 (Ablation Study)
*Lưu ý: Trong câu hỏi nghiên cứu, bảng này đôi khi được gọi nhầm là Table 3, nhưng trong bản PDF gốc của Retinexformer, nghiên cứu bóc tách nằm ở **Table 4 (Trang 8)**.*

Nghiên cứu bóc tách (Ablation Study) trả lời câu hỏi: *"Các bộ phận đắt giá mà tác giả đề xuất (khung ORF và cơ chế chú ý IG-MSA) thực sự đóng góp bao nhiêu vào thành công chung, hay chỉ làm nặng thêm mô hình?"* Tác giả thực hiện nghiên cứu này trên bộ dữ liệu **SDSD-outdoor**.

#### Table 4a: Thử nghiệm bóc tách từng phần (Break-down Ablation)
*   **Dòng 1 (Baseline-1):** Loại bỏ cả ORF và IG-MSA (chỉ còn mạng Transformer cơ bản phục hồi ảnh). Kết quả đạt **26.47 dB**.
*   **Dòng 2 (Chỉ thêm ORF):** PSNR tăng vọt lên **27.92 dB** (+1.45 dB). Chứng minh việc mô hình hóa nhiễu thông qua ORF cực kỳ hiệu quả.
*   **Dòng 3 (Chỉ thêm IG-MSA):** PSNR tăng lên **28.86 dB** (+2.39 dB). Chứng minh cơ chế tự chú ý dẫn đường bằng ánh sáng hoạt động cực tốt.
*   **Dòng 4 (Kết hợp cả ORF + IG-MSA - Retinexformer đầy đủ):** Đạt PSNR cao nhất **29.84 dB** (tăng tổng cộng **3.37 dB** so với Baseline-1).
*   **Kết luận:** Cả hai thành phần đều đóng vai trò cốt lõi và có tính tương hỗ mạnh mẽ.

#### Table 4b: Đánh giá cơ chế Light-up trong khung ORF
*   Tác giả chứng minh rằng việc sử dụng phép nhân với bản đồ chiếu sáng ngược dòng ($\bar{L}$) hiệu quả hơn nhiều so với phép chia truyền thống ($I./L$) vốn dễ lỗi toán học khi gặp giá trị gần bằng 0 (đạt **29.26 dB** so với **28.97 dB**).
*   Khi tích hợp thêm luồng đặc trưng ánh sáng hướng dẫn ($F_{lu}$), mô hình đạt đỉnh cao **29.84 dB**.

#### Table 4c: Đánh giá cơ chế tự chú ý IG-MSA
*   Tác giả so sánh IG-MSA do mình tự thiết kế với các cơ chế tự chú ý nổi tiếng khác: **Global MSA (G-MSA)** và **Local Window MSA (W-MSA)** của Swin Transformer.
*   **Kết quả:** IG-MSA đạt **29.84 dB** (vượt G-MSA 1.41 dB và vượt W-MSA 1.34 dB).
*   **Đặc biệt về hiệu năng:** IG-MSA tiêu tốn ít FLOPS hơn cả hai đối thủ (chỉ 15.57G so với 17.65G của G-MSA và 16.43G của W-MSA). Đây là minh chứng đập tan định kiến "Transformer luôn nặng nề".

---

## 3. Từ điển giải nghĩa thuật ngữ "khó hiểu"
*Dưới đây là bảng giải nghĩa bình đơn giản các thuật ngữ học thuật xuất hiện trong chương thực nghiệm:*

| Thuật ngữ chuyên ngành | Giải nghĩa đơn giản, dễ nhớ | Ý nghĩa trong nghiên cứu LLIE |
| :--- | :--- | :--- |
| **PSNR** *(Peak Signal-to-Noise Ratio)* | **Tỷ số tín hiệu cực đại trên nhiễu** (dB). Đo xem ảnh đầu ra có bị lệch màu hay sai khác pixel so với ảnh chuẩn (Ground Truth) không. | **Càng cao càng tốt.** Ảnh tăng cường có PSNR > 25 dB được coi là có chất lượng phục hồi cấu trúc và màu sắc rất tốt. |
| **SSIM** *(Structural Similarity Index)* | **Chỉ số tương đồng cấu trúc**. Đo độ giống nhau về độ chói, tương phản và chi tiết hình học của ảnh đầu ra so với ảnh chuẩn. | **Giá trị từ 0 đến 1 (càng gần 1 càng tốt).** SSIM cao nghĩa là các đường nét, rìa vật thể và kết cấu bề mặt được bảo toàn hoàn hảo. |
| **LPIPS** *(Learned Perceptual Image Patch Similarity)* | **Độ tương đồng cảm nhận trực quan học được**. Một chỉ số dùng mạng Deep Learning để chấm điểm xem bức ảnh trông có "thuận mắt người" không. | **Càng thấp càng tốt.** Điểm LPIPS thấp đồng nghĩa với việc bức ảnh trông tự nhiên và có tính thẩm mỹ cao đối với con người. |
| **Ablation Study** | **Nghiên cứu bóc tách/thử nghiệm loại trừ**. Giống như việc tháo từng bộ phận của chiếc xe máy ra để xem thiếu nó thì xe có chạy được không. | Giúp chứng minh tính trung thực khoa học, khẳng định các khối kiến trúc đề xuất thực sự có tác dụng chứ không phải do ăn may. |
| **SOTA** *(State-Of-To-Art)* | **Trạng thái công nghệ tiên tiến nhất**. Kẻ đang thống trị đỉnh cao về mặt hiệu năng trên thế giới tại thời điểm công bố. | Retinexformer chứng minh mình là SOTA mới bằng cách vượt qua các SOTA cũ trên 13 bộ dữ liệu. |
| **Params** *(Parameters)* | **Số lượng tham số học được (Trọng số)**. Tượng trưng cho độ lớn/dung lượng bộ nhớ cần thiết để lưu trữ mô hình AI. | **Càng nhỏ càng tốt.** Mẫu Retinexformer cực nhẹ chỉ có 1.61M Params (trong khi các mẫu Transformer khác thường nặng hàng chục đến hàng trăm triệu tham số). |
| **FLOPs** *(Floating Point Operations)* | **Số phép tính dấu phẩy động**. Đo lượng công việc tính toán mà GPU/CPU phải làm để xử lý xong một bức ảnh. | **Càng nhỏ càng tốt.** Đo lường tốc độ nhanh/chậm của thuật toán. Retinexformer có FLOPS thấp nên rất hứa hẹn cho các ứng dụng thực tế. |
| **Ground Truth (GT)** | **Ảnh thực chứng / Ảnh tiêu chuẩn**. Bức ảnh chụp trong điều kiện hoàn hảo (đủ sáng, phơi sáng lâu, không nhiễu) dùng làm đáp án chuẩn. | Là cái đích mà mô hình tăng cường ảnh luôn phải cố gắng tái tạo giống hệt. |

---

## 4. Hướng dẫn đọc hiểu bảng biểu và hình ảnh
*Chỉ dẫn chi tiết cách đối chiếu số liệu và hình ảnh trực quan trong file PDF Retinexformer bằng mắt thường.*

Để bài luận văn tốt nghiệp của bạn có những lập luận sắc bén và chân thực, hãy mở file PDF gốc của Retinexformer và đối chiếu trực tiếp các hình ảnh sau:

### 4.1. Đối chiếu định lượng (Quantitative Proofs)
*   **Bước 1:** Tìm đến **Table 1 (Trang 6)**. Nhìn vào cột **LOL-v1**. Hãy so sánh điểm số PSNR của các phương pháp cũ như **RetinexNet (16.77 dB)**, **KinD (20.86 dB)** với **Retinexformer (25.16 dB)**. Khoảng cách chênh lệch lên tới gần **8.4 dB**! Đây là một con số khổng lồ trong xử lý ảnh.
*   **Bước 2:** Nhìn vào hai cột cuối cùng của Table 1 (`Complexity`). So sánh **Restormer** (Params: `26.13M`, FLOPS: `144.25G`) với **Retinexformer** (Params: `1.61M`, FLOPS: `15.57G`). Hãy nhấn mạnh trong luận văn của bạn rằng: *Retinexformer đạt chất lượng vượt trội nhưng nhẹ hơn đối thủ tới 16 lần về tham số và 9 lần về lượng tính toán.*

### 4.2. Đối chiếu trực quan bằng mắt thường (Qualitative/Visual Proofs)
Hãy mở các hình ảnh trực quan sinh động trong PDF để thấy sự khác biệt:

#### 1. Figure 3 (Trang 5): Thử nghiệm trên LOL-v1 & LOL-v2
*   **Cảnh dòng trên (LOL-v1):** Quan sát khu vực bức tường và các chi tiết tối. 
    *   **RUAS** bị hiện tượng ám màu vàng/đỏ cực kỳ nặng nề và mất tự nhiên.
    *   **RetinexNet** bị cháy sáng và nhiễu hạt vỡ vụn.
    *   **Retinexformer** tái tạo màu sắc của bức tường vô cùng mịn màng, ấm áp và chân thực như ảnh Ground Truth.
*   **Cảnh dòng dưới (LOL-v2):** Nhìn vào chi tiết kệ sách hoặc tủ đồ. Retinexformer giữ được các đường nét chữ viết và ranh giới đồ vật sắc nét nhất.

#### 2. Figure 4 (Trang 6): Thử nghiệm trên ảnh RAW cực tối (SID & SMID)
*   Hãy phóng to (zoom in) **Figure 4**. 
    *   Các phương pháp phục hồi ảnh siêu mạnh như **Restormer** hay **SNR-Net** vẫn để lại các vết mờ (blur) và nhiễu màu loang lổ ở vùng tối sâu do không mô hình hóa tốt nhiễu trong quá trình làm sáng.
    *   **Retinexformer** nhờ có mô hình nhiễu tích hợp trong ORF đã khử sạch các hạt nhiễu sắc màu, trả lại các chi tiết nhỏ sắc nét (nhìn rõ các ký tự hoặc vân gỗ).

#### 3. Figure 5 (Trang 7): Thử nghiệm trên video SDSD (indoor & outdoor)
*   Quan sát khu vực bầu trời đêm ở dòng dưới (SDSD-outdoor). 
    *   Bạn sẽ thấy **EnlightenGAN** hay **SNR-Net** xuất hiện các đốm đen loang lổ kỳ dị (black spot corruptions) và hiện tượng giả tạo (unnatural artifacts) rất khó chịu.
    *   **Retinexformer** cho ra một bầu trời mịn màng, chuyển sắc tự nhiên và cấu trúc tòa nhà bên dưới được giữ vững cấu trúc hình học.

#### 4. Figure 6 (Trang 7): Ứng dụng phát hiện vật thể (ExDark)
*   Nhìn vào **Figure 6** để thấy ứng dụng thực tiễn của mô hình. 
    *   Bên trái là ảnh thiếu sáng gốc, mô hình YOLO-v3 hoàn toàn bị "mù", bỏ sót rất nhiều thuyền bè trên sông hoặc định vị sai lệch vị trí.
    *   Bên phải là ảnh sau khi đi qua Retinexformer, các con thuyền ẩn sâu trong bóng tối được hiện rõ mồn một giúp YOLO-v3 vẽ khung bao (bounding box) cực kỳ chính xác. Đây là bằng chứng đanh thép chứng minh giá trị của Retinexformer đối với các hệ thống thị giác thông minh.

---

> [!TIP]
> **Lời khuyên khi viết luận văn tốt nghiệp:** Khi trích dẫn chương thực nghiệm này, bạn hãy nhấn mạnh tính **toàn diện** của nghiên cứu. Tác giả không chỉ thắng trên lý thuyết toán học (PSNR/SSIM) mà còn thắng ở cảm quan con người (User Study), hiệu quả phần cứng (Complexity) và ứng dụng thực tế (Object Detection). Điều này làm nên giá trị khoa học vô cùng bền vững cho Retinexformer.
