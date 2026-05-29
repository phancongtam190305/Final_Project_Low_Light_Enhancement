# Bước 1: Phân Loại Các Nhánh Trong Bài Toán Low-Light Image Enhancement (LLIE)

Để chốt phạm vi bài toán cho đồ án tốt nghiệp, bước đầu tiên là chúng ta cần hiểu rõ bài toán LLIE được chia thành những nhánh nghiên cứu nào, mục tiêu của từng nhánh và các bộ dữ liệu đi kèm.

---

## 📊 Bảng Tổng Hợp Phân Loại Các Nhánh Nghiên Cứu

| Nhánh Nghiên Cứu | Mục Tiêu Chính | Dataset Thường Dùng |
| :--- | :--- | :--- |
| **Paired enhancement** | Khôi phục ảnh thiếu sáng sang ảnh đủ sáng bình thường dựa trên dữ liệu cặp (Low $\rightarrow$ Normal). | [LOL](https://www.kaggle.com/datasets/soumikrakshit/lol-dataset), [LOL-v2](https://www.kaggle.com/datasets/tanhyml/lol-v2-dataset), [SID](https://www.kaggle.com/datasets/marcorosato/sid-dataset), [SICE-p1](https://drive.google.com/file/d/1HiLtYiyT9R7dR9DRTLRlUUrAicC4zzWN/view?pli=1) |
| **Unpaired / zero-reference** | Tăng cường ánh sáng không cần cặp ảnh ground truth chuẩn để huấn luyện. | [DICM](https://github.com/Li-Chongyi/Zero-DCE), [LIME](https://github.com/weichen582/LIME), [MEF](https://github.com/Li-Chongyi/Zero-DCE), [NPE](https://github.com/Li-Chongyi/Zero-DCE) |
| **RAW low-light** | Phục hồi ảnh trực tiếp từ dữ liệu cảm biến RAW bị cực tối và nhiễu (noise) nặng. | [SID](https://cchen156.github.io/SeeInTheDark.html), [SDSD](https://github.com/flyywh/Awesome-Low-Light-Enhancement), [SMID](https://github.com/flyywh/Awesome-Low-Light-Enhancement) |
| **Real-world high-res** | Tăng cường ảnh trong điều kiện thực tế (độ phân giải 2K/4K, ngược sáng - backlight, ánh sáng không đồng đều). | [NTIRE LLIE](https://github.com/cvpr-ntire-llie) |
| **LLIE cho downstream task** | Tăng cường ảnh nhằm mục đích cải thiện độ chính xác cho các tác vụ tiếp theo (như object detection, segmentation). | [ExDark](https://github.com/cs-chan/Exclusively-Dark-Image-Dataset), [LoLI-Street](https://github.com/tanvirnwu/TriFuse), [LLVIP](https://bupt-ai-cz.github.io/LLVIP/) |

---

## 🔍 Phần 2: Phân Tích Chuyên Sâu Từng Hướng Đi

Dưới đây là phân tích chi tiết về 5 hướng nghiên cứu lớn trong bài toán Low-Light Image Enhancement để giúp bạn có cái nhìn sâu sắc trước khi đưa ra quyết định chọn đề tài.

### 1. Paired Enhancement (Học có giám sát trên ảnh RGB cặp)
* **Bản chất kỹ thuật**: Mạng nơ-ron học cách ánh xạ trực tiếp từng pixel từ ảnh đầu vào tối (RGB) sang ảnh đầu ra sáng chuẩn (Ground Truth RGB).
* **Ưu điểm lớn (Pros)**: 
  * Độ chính xác cực kỳ cao trên tập dữ liệu đã được học.
  * Các chỉ số định lượng như **PSNR** và **SSIM** đạt mức tối ưu nhất vì mô hình có mục tiêu so sánh trực tiếp (ground truth) để tối ưu hóa lỗi (loss).
* **Thách thức lớn (Cons)**: 
  * *Vấn đề dữ liệu:* Việc chụp được hai bức ảnh tĩnh giống hệt nhau về bố cục (cảnh động, rung tay) nhưng chỉ khác biệt về độ sáng ngoài thực tế là cực kỳ khó khăn.
  * *Tính tổng quát hóa (Generalization) kém:* Mô hình được huấn luyện trên một dataset cụ thể (ví dụ: LOL Dataset trong phòng) thường hoạt động rất tệ khi test trên các ảnh chụp đêm ngoài đường phố thực tế.
* **Kiến trúc tiêu biểu**: RetinexNet, KinD, MIRNet, Restormer, Retinexformer.
* **Đánh giá Đồ án Tốt nghiệp**:
  * **Độ khó thực hiện**: 2.5 / 5 (Rất nhiều mã nguồn mở chạy ổn định, dễ benchmark).
  * **Tài nguyên GPU**: Vừa phải đến Khá (Các mô hình Transformer như Restormer sẽ cần GPU mạnh hơn).
  * **Tiềm năng đạt điểm cao**: Trung bình - Khá (Đây là hướng đi truyền thống, bạn cần cải tiến kiến trúc hoặc hàm loss rõ ràng để tạo điểm mới).

---

### 2. Unpaired / Zero-Reference (Học không giám sát & Zero-shot)
* **Bản chất kỹ thuật**: Mô hình không cần bất kỳ cặp ảnh thiếu sáng/đủ sáng nào để học. Thay vào đó, nó học thông qua các hàm loss vật lý đặc thù (Spatial Consistency, Exposure Control, Color Constancy) hoặc thông qua mạng sinh đối kháng (GAN) để biến đổi phong cách ảnh.
* **Ưu điểm lớn (Pros)**:
  * Không tốn chi phí và công sức thu thập cặp ảnh Ground Truth.
  * Có thể huấn luyện trực tiếp trên mọi nguồn ảnh thực tế thu thập được trên Internet.
  * Các mô hình Zero-shot (như Zero-DCE) có tốc độ suy diễn cực kỳ nhanh, mô hình siêu nhẹ.
* **Thách thức lớn (Cons)**:
  * Vì không có ảnh Ground Truth để định hướng, ảnh đầu ra đôi khi bị sai lệch màu sắc (color cast) hoặc bị mất chi tiết ở những vùng quá tối.
  * Chỉ số PSNR/SSIM thường không cao (vì không có GT chuẩn để so sánh chéo). Thay vào đó phải đánh giá bằng thị giác người dùng hoặc các metric không tham chiếu (NIQE).
* **Kiến trúc tiêu biểu**: EnlightenGAN, Zero-DCE, Zero-DCE++, SCI (Self-Calibrated Illumination).
* **Đánh giá Đồ án Tốt nghiệp**:
  * **Độ khó thực hiện**: 3.5 / 5 (Cần hiểu sâu về thiết kế Loss Function phi tham chiếu).
  * **Tài nguyên GPU**: Rất nhẹ (Zero-DCE có thể huấn luyện hoàn chỉnh chỉ trong 10-30 phút trên GPU thông thường).
  * **Tiềm năng đạt điểm cao**: Rất cao (Đặc biệt phù hợp nếu đồ án của bạn hướng tới ứng dụng thực tế trên thiết bị di động/nhúng nhờ tốc độ thời gian thực).

---

### 3. RAW Low-Light (Phục hồi từ dữ liệu thô cảm biến)
* **Bản chất kỹ thuật**: Xử lý trực tiếp tín hiệu số thô (Bayer pattern) xuất ra từ cảm biến máy ảnh trước khi đi qua bộ xử lý ảnh phần cứng (ISP - Image Signal Processor). Mạng nơ-ron sẽ đóng vai trò như một bộ ISP học sâu để vừa tăng sáng, vừa khử nhiễu nặng, vừa hiệu chỉnh màu sắc.
* **Ưu điểm lớn (Pros)**:
  * Lưu giữ được thông tin vật lý thô của ánh sáng mà không bị suy hao hay nén nứt như ảnh RGB thường.
  * Khôi phục được những bức ảnh chụp trong điều kiện cực kỳ tối (gần như đen kịt hoàn toàn) mà ảnh JPG/RGB thông thường không có khả năng cứu vãn do thiếu thông tin.
* **Thách thức lớn (Cons)**:
  * Dung lượng ảnh RAW cực kỳ nặng (20MB - 50MB/ảnh), yêu cầu bộ nhớ GPU rất lớn khi huấn luyện.
  * Đòi hỏi kiến thức sâu về xử lý ảnh số truyền thống (demosaicing, white balance, gamma correction) để thiết kế pipeline.
* **Kiến trúc tiêu biểu**: SID (See-in-the-Dark), SDSD, LambaNet.
* **Đánh giá Đồ án Tốt nghiệp**:
  * **Độ khó thực hiện**: 4.5 / 5 (Khó debug, tiền xử lý dữ liệu phức tạp).
  * **Tài nguyên GPU**: Yêu cầu rất cao (GPU dung lượng VRAM lớn).
  * **Tiềm năng đạt điểm cao**: Xuất sắc (Mang tính học thuật rất cao, dễ thuyết phục các thầy cô trong hội đồng khoa học chấm điểm tối đa).

---

### 4. Real-world High-Res (Tăng sáng ảnh siêu phân giải & thực tế)
* **Bản chất kỹ thuật**: Tập trung giải quyết các bài toán "gai góc" ngoài đời thực: ảnh siêu nét 2K/4K, ảnh bị ngược sáng (backlight), ảnh có vùng tối vùng sáng xen kẽ phức tạp không đều (non-uniform illumination).
* **Ưu điểm lớn (Pros)**:
  * Khắc phục triệt để điểm yếu của các mô hình LLIE lý thuyết (thường chỉ hoạt động tốt trên ảnh nhỏ 400x600 và ánh sáng tối đều).
  * Tính thực tiễn cực kỳ cao cho các thiết bị chụp ảnh cao cấp hiện nay.
* **Thách thức lớn (Cons)**:
  * Bộ nhớ GPU tăng phi mã khi xử lý ảnh độ phân giải cao 4K.
  * Thuật toán phải đủ thông minh để tăng sáng vùng tối mà không làm cháy (over-exposure) vùng vốn đã sáng sẵn.
* **Kiến trúc tiêu biểu**: Các giải pháp đoạt giải trong cuộc thi NTIRE Challenge (2024/2025).
* **Đánh giá Đồ án Tốt nghiệp**:
  * **Độ khó thực hiện**: 4.0 / 5.
  * **Tài nguyên GPU**: Khá cao (để xử lý ảnh độ phân giải cao).
  * **Tiềm năng đạt điểm cao**: Xuất sắc (Hướng đi mang tính cập nhật công nghệ mới nhất hiện nay).

---

### 5. LLIE cho Downstream Task (Tác vụ bổ trợ thị giác máy tính)
* **Bản chất kỹ thuật**: Tăng cường chất lượng ảnh không phải để cho mắt người nhìn đẹp, mà là để làm đầu vào (tiền xử lý) cho một mô hình thị giác máy tính khác (Object Detection, Semantic Segmentation) chạy phía sau.
* **Ưu điểm lớn (Pros)**:
  * Giải quyết trực tiếp một ứng dụng thực tế quan trọng: giúp camera an ninh, hệ thống xe tự lái phát hiện được vật thể, người đi bộ, làn đường một cách chính xác trong đêm tối.
  * Có hệ thống đánh giá định lượng cực kỳ thực tế bằng độ chính xác của tác vụ sau (chỉ số **mAP** cho Detection, **mIoU** cho Segmentation).
* **Thách thức lớn (Cons)**:
  * Đồ án sẽ trở nên phức tạp hơn vì bạn phải xử lý đồng thời 2 mô hình (Mô hình Enhancement + Mô hình Downstream).
  * Đôi khi ảnh được tăng cường trông rất xấu đối với mắt người (nhiễu, bệt màu) nhưng lại giúp mô hình Object Detection nhận diện vật thể tốt hơn rất nhiều.
* **Kiến trúc tiêu biểu**: TriFuse (ACCV 2024), các pipeline kết hợp Zero-DCE + YOLOv8.
* **Đánh giá Đồ án Tốt nghiệp**:
  * **Độ khó thực hiện**: 4.0 / 5.
  * **Tài nguyên GPU**: Khá cao (huấn luyện song song hoặc tuần tự cả mạng tăng sáng lẫn mạng nhận diện).
  * **Tiềm năng đạt điểm cao**: Xuất sắc (Hướng đi cực kỳ được ưa chuộng vì tính thực dụng cao và có ứng dụng thương mại rõ ràng).

---

## 🎯 Chốt Phạm Vi Nghiên Cứu Đồ Án Của Bạn

> [!IMPORTANT]
> **Câu hỏi định hướng đồ án:** Đồ án tốt nghiệp của bạn dự kiến sẽ tập trung vào loại hình nào dưới đây?
>
> *(Bạn có thể điền dấu `[x]` vào lựa chọn mong muốn dưới đây hoặc ghi chép trực tiếp vào file này)*

- [ ] **Nhóm A: Tăng cường chất lượng ảnh thuần túy (Image Enhancement)**
  * *Mục tiêu:* Tập trung vào khôi phục màu sắc, tăng độ tương phản, khử nhiễu, giúp ảnh đầu ra trông tự nhiên và đẹp mắt nhất có thể đối với mắt người (chỉ số đánh giá chính là PSNR, SSIM, LPIPS).
  
- [ ] **Nhóm B: Tăng cường phục vụ tác vụ phụ trợ (Enhancement cho Downstream Tasks)**
  * *Mục tiêu:* Tăng cường ảnh thiếu sáng để cải thiện kết quả cho các mô hình Object Detection (phát hiện vật thể), Segmentation (phân vùng ảnh), hoặc Tracking (theo dõi vật thể) chạy phía sau trong môi trường đêm (chỉ số đánh giá chính là mAP, IoU...).
