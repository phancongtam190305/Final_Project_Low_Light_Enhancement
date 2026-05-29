# Khảo Sát Tập Dữ Liệu Nhánh 5: LLIE Cho Downstream Tasks

Tài liệu này thực hiện khảo sát chi tiết và hệ thống hóa thông tin khoa học của các tập dữ liệu cốt lõi phục vụ cho bài toán Tăng cường Ảnh Thiếu Sáng tích hợp Tác vụ Hạ nguồn (Low-Light Image Enhancement for Downstream Tasks - Nhánh 5). Các tập dữ liệu được khảo sát bao gồm: **ExDark (Exclusively Dark)**, **LLVIP (Visible-Infrared Paired)**, **LoLI-Street (Low-Light Images of Streets)** và **DARK FACE (UG2+ Challenge)**.

---

## 1. Bảng 1: Thông Tin Cơ Bản (Basic Information)

Bảng này cung cấp các thông tin nền tảng về nguồn gốc lịch sử, quy mô dữ liệu, định dạng vật lý, tác vụ mục tiêu và tính pháp lý của từng tập dữ liệu trong nhánh tác vụ hạ nguồn.

| Tiêu Chí | ExDark (Exclusively Dark) | LLVIP (Visible-Infrared Paired) | LoLI-Street (ACCV 2024 Benchmark) | DARK FACE (UG2+ Challenge) |
| :--- | :--- | :--- | :--- | :--- |
| **Năm công bố** | 2019 | 2021 | 2024 | 2019 / 2020 |
| **Hội nghị / Tạp chí** | Elsevier CVIU 2019 | IEEE ICCV Workshops 2021 | ACCV 2024 | CVPR Workshops (UG2+) |
| **Nhóm tác giả / Đơn vị** | Yuen Peng Loh, Cheah Wooi Guan, Chan Chee Seng <br>*(University of Malaya)* | Xinyu Jia, Chao Xiao, Guanzhou Wu, Yohei Sotooka, Jizhou Li <br>*(BUPT & CityU Hong Kong)* | Tanvir Ahmed, et al. <br>*(Northwest University, China)* | Wenhan Yang, et al. <br>*(Peking University & partners)* |
| **Link download chính thức** | [ExDark GitHub](https://github.com/cs-chan/ExDark) | [LLVIP Repository](https://github.com/bupt-ai-cz/LLVIP) | [LoLI-Street Link](https://github.com/tanvirnwu/TriFuse) | [DARK FACE Project](https://flyyufelix.github.io/2019/04/16/ug2-challenge.html) |
| **Tổng số lượng ảnh** | 7,363 ảnh đơn kênh sRGB | 15,488 cặp ảnh (30,976 ảnh đơn gồm 15,488 Visible + 15,488 Infrared) | 34,000 ảnh (30k Train cặp + 3k Val cặp + 1k RLLT Test đơn thực tế) | 6,000 ảnh gán nhãn + 9,000 ảnh không nhãn + 4,000 ảnh Test giấu nhãn + 789 cặp thực tế |
| **Phân chia Train / Val / Test** | Thường chia theo tỷ lệ tự chọn:<br>- 80% Train & Val (5,890 ảnh)<br>- 20% Test (1,473 ảnh) | Phân chia chính thức:<br>- 12,025 cặp Train (24,050 ảnh)<br>- 3,463 cặp Test (6,926 ảnh) | Phân chia chính thức:<br>- 30,000 cặp Train<br>- 3,000 cặp Validation<br>- 1,000 ảnh Real Test (RLLT) | Phân chia chính thức:<br>- 6,000 Train/Val (thường chia 5k Train / 1k Val)<br>- 4,000 Test (Hold-out) |
| **Độ phân giải (Resolution)**| Không đồng đều (Ảnh thu thập thực tế từ Internet, trung bình $400\times300$ đến $1000\times800$) | Đồng bộ hóa nghiêm ngặt:<br>- Visible: $1920\times1080$ pixels<br>- Infrared: $1280\times720$ pixels | Độ phân giải cao gốc từ video 4K/8K (Hỗ trợ cắt patch hoặc huấn luyện kích thước tùy chỉnh) | Độ phân giải cao $1920\times1080$ pixels (Đồng đều trên toàn bộ tập dữ liệu) |
| **Định dạng dữ liệu** | sRGB (JPG, 8-bit) | sRGB (JPG cho Visible; PNG/JPG 8-bit cho Infrared grayscale) | sRGB (PNG/JPG, 8-bit) | sRGB (PNG/JPG, 8-bit) |
| **Bản quyền (License)** | Sử dụng học thuật phi thương mại | Creative Commons Attribution 4.0 | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại (UG2+ Challenge) |
| **Tác vụ Downstream chính** | Phát hiện đối tượng thiếu sáng (Low-light Object Detection - 12 lớp) | Phát hiện người đi bộ ban đêm (Pedestrian Detection) & Image Fusion | Phát hiện đối tượng đường phố (Urban Object Detection - YOLOv8/v9/v10) | Phát hiện khuôn mặt ban đêm (Nighttime Face Detection) |

---

## 2. Bảng 2: Đặc Tính Kỹ Thuật (Technical Characteristics)

Bảng này phân tích sâu các khía cạnh kỹ thuật liên quan đến phương pháp thu thập dữ liệu, cơ chế phơi sáng, căn chỉnh pixel, đặc tính nhiễu cảm biến và tính phong phú của nhãn hạ nguồn (downstream annotations).

| Tiêu Chí Kỹ Thuật | ExDark (Exclusively Dark) | LLVIP (Visible-Infrared Paired) | LoLI-Street (ACCV 2024 Benchmark) | DARK FACE (UG2+ Challenge) |
| :--- | :--- | :--- | :--- | :--- |
| **Thiết bị chụp / Quy trình tạo** | Chụp thực tế từ nhiều dòng camera tiêu dùng (smartphones, DSLRs) thông qua cào dữ liệu Flickr/Web. | Chụp thực tế bằng hệ thống camera giám sát tầm xa quang-hồng ngoại kép lắp đặt cố định ngoài trời. | Trích xuất khung hình từ video độ phân giải siêu cao (4K/8K @ 60fps) đường phố thực tế; cặp ảnh tối-sáng được tạo tổng hợp qua Photoshop v25.0. | Chụp thực tế tại các bối cảnh ngoại cảnh ban đêm sử dụng nhiều loại máy ảnh cơ học cầm tay. |
| **Cơ chế chiếu sáng (Illumination)** | 10 môi trường ánh sáng yếu thực tế: Low, Ambient, Object, Single, Weak, Strong, Window, Screen, Shadow, Twilight. | Ánh sáng đường phố ban đêm cực tối (surveillance lighting) kết hợp cảm biến hồng ngoại nhiệt dải sóng 8~14µm. | 3 mức độ thiếu sáng nhân tạo mô phỏng đường phố đô thị: High, Moderate, Light. Kèm 1,000 ảnh thật thiếu sáng hoàn toàn (RLLT). | Ánh sáng ban đêm cực đoan thực tế ngoài trời (gần như bằng 0 hoặc chỉ có nguồn sáng khuếch tán rất yếu từ xa). |
| **Phương pháp tạo nhãn hạ nguồn** | Gán nhãn thủ công hộp giới hạn (Bounding Box) cho 12 lớp đối tượng phổ biến trong đời sống. | Hỗ trợ gán nhãn người đi bộ trên ảnh hồng ngoại (nơi người phát xạ nhiệt rõ nét), sau đó ánh xạ đồng bộ sang ảnh Visible. | Gán nhãn thủ công theo chuẩn định dạng YOLO cho các đối tượng đường phố (bao gồm 19,000 lớp nhãn tích hợp từ video nguồn). | Gán nhãn thủ công bounding box vị trí khuôn mặt người đi bộ tại các khu vực tối tăm. |
| **Căn chỉnh ảnh (Alignment)** | Không có ảnh cặp đủ sáng (Unpaired). Chỉ có ảnh thiếu sáng kèm hộp giới hạn. | Căn chỉnh pixel-wise đồng bộ cực kỳ nghiêm ngặt giữa camera visible và hồng ngoại nhiệt qua đăng ký ảnh hình học cơ học. | Đạt độ căn chỉnh pixel tuyệt đối (100% khớp) ở tập Train/Val tổng hợp do sinh ra từ cùng một ảnh gốc tĩnh. | Không có ảnh cặp đủ sáng cho tập gán nhãn lớn (chỉ có 789 cặp chụp kiểm soát để hiệu chuẩn). |
| **Đặc tính Nhiễu (Noise & Artifacts)**| Nhiễu cảm biến thực tế phức tạp, hạt nhiễu (sensor noise) màu loang lổ, độ nhòe chuyển động do chụp cầm tay tốc độ màn trập thấp. | Nhiễu cảm biến giám sát chuẩn công nghiệp, nhiễu nén luồng truyền video (compression artifacts) trên kênh Visible. | Tập Train/Val tổng hợp không có nhiễu cảm biến thực tế, nhưng tập Real Test (RLLT) chứa nhiễu hạt gắt và nhòe động rất nặng. | Nhiễu hạt cực kỳ nặng, nhiễu nhiệt cảm biến, mất chi tiết cấu trúc cục bộ và quầng tối sâu hoắm. |
| **Độ đa dạng bối cảnh** | Cực cao. Bao gồm bối cảnh trong nhà, ngoài trời, tĩnh vật, con người, giao thông và động vật dưới nhiều nguồn sáng phức tạp. | Trung bình. Giới hạn trong các góc quay an ninh cố định tầm trung tại các ngõ nhỏ, sân trường, khu dân cư về đêm. | Rất cao. Phủ khắp các đô thị phát triển, đường phố, phương tiện giao thông di chuyển tốc độ cao, biển báo và đèn đường hiệu ứng động. | Rất cao về mặt địa điểm ngoại cảnh đêm (công viên, đường phố hẻo lánh, khuôn viên trường đại học) nhưng chỉ chứa con người. |
| **Số lượng lớp đối tượng** | 12 lớp cụ thể: Bicycle, Boat, Bottle, Bus, Car, Cat, Chair, Cup, Dog, Motorbike, People, Table. | 1 lớp duy nhất: Người đi bộ (Pedestrian / Person). | 19,000 lớp đối tượng hạ nguồn (Được benchmark trên 7 lớp chính: Person, Bicycle, Car, Motorcycle, Bus, Traffic Light, Street Sign). | 1 lớp duy nhất: Khuôn mặt người (Face). |

---

## 3. Bảng 3: Giao Thức & Đánh Giá (Protocol & Evaluation)

Bảng này cung cấp các tiêu chuẩn đánh giá định lượng hạ nguồn, phân chia dữ liệu mặc định và hiệu năng hạ nguồn cơ sở (downstream baseline performance) của các phương pháp phục hồi ảnh thiếu sáng đi trước.

| Tiêu Chí Đánh Giá | ExDark (Exclusively Dark) | LLVIP (Visible-Infrared Paired) | LoLI-Street (ACCV 2024 Benchmark) | DARK FACE (UG2+ Challenge) |
| :--- | :--- | :--- | :--- | :--- |
| **Phân chia dữ liệu mặc định** | Thường dùng 80% (5,890 ảnh) để Train/Val mạng detector, và 20% (1,473 ảnh) để đánh giá độ chính xác mAP. | 12,025 cặp ảnh dùng để huấn luyện detector đa phương thức; 3,463 cặp ảnh độc lập dùng để test hiệu năng mAP. | 30,000 cặp huấn luyện mạng tăng cường; 3,000 cặp kiểm định; 1,000 ảnh Real Test (RLLT) dùng để kiểm tra độ tương thích downstream thực tế. | 6,000 ảnh dùng huấn luyện và kiểm định chéo cục bộ; 4,000 ảnh test gửi lên server UG2+ Challenge để chấm điểm giấu nhãn. |
| **Sự chồng chéo bối cảnh** | Không chồng chéo bối cảnh nếu sử dụng bộ lọc phân chia ảnh theo ID nguồn ảnh gốc từ web. | **Không chồng chéo địa lý**. Tập huấn luyện và tập test được chụp tại các địa điểm và camera vật lý tách biệt hoàn toàn. | **Không chồng chéo**. Đảm bảo năng lực tổng quát hóa tuyệt đối của các mô hình Enhancement và Detector. | Thấp. Các bối cảnh được chụp độc lập tại nhiều đêm và địa điểm địa lý khác nhau. |
| **Mô hình Downstream tiêu biểu** | YOLOv3, YOLOv5, YOLOv8, YOLOv9, Faster R-CNN, Deformable DETR. | YOLOv5 (Visible/IR), YOLOv8-Dual Branch, CFT (Cross-Modality Fusion Transformer), Pedestrian Detectors. | YOLOv8, YOLOv9, YOLOv10 (Được sử dụng làm mạng phát hiện chuẩn trong bài báo TriFuse). | DSFD (Dual Shot Face Detector), RetinaFace, HLA-Face (High-Low Adaptation Face Detector). |
| **Metrics đánh giá chính** | mean Average Precision (**mAP@0.5** và **mAP@0.5:0.95**) cho 12 lớp đối tượng. | mAP@0.5, mAP@0.5:0.95 và Log-average Miss Rate ($MR^{-2}$) đối với phát hiện người đi bộ. | PSNR, SSIM, LPIPS (đánh giá thị giác vùng Train/Val); BRISQUE, NIQE (đánh giá ảnh thật RLLT); **mAP(0.5)** và **mAP(0.5-0.9)** cho downstream. | Average Precision (**AP**) ở IoU threshold = 0.5 đối với phát hiện khuôn mặt ban đêm. |
| **Giao thức tiền xử lý dữ liệu** | Resize ảnh về kích thước chuẩn ($416\times416$ hoặc $640\times640$), áp dụng chuẩn hóa pixel sRGB và các kỹ thuật augmentation (mixup, mosaic). | Resize ảnh Visible và IR về $640\times640$, đăng ký căn khớp ma trận homography pixel, căn lề đồng bộ hóa nhãn bboxes. | Cắt patch ảnh kích thước $256\times256$ pixel trong quá trình huấn luyện tăng sáng; resize về kích thước mạng YOLO khi chạy tác vụ phát hiện. | Đưa ảnh gốc chất lượng cao $1920\times1080$ qua mô-đun LLIE tiền xử lý, sau đó cấp trực tiếp vào mạng Face Detector. |
| **Hiệu năng Downstream Baseline** | - **Chưa tăng sáng (Raw)**: ~70.5% mAP@0.5<br>- **Zero-DCE + YOLOv8**: ~71.8% mAP@0.5<br>- **SCI + YOLOv8**: ~72.5% mAP@0.5<br>- **Dark-YOLO**: ~73.9% mAP@0.5 | - **Visible Raw + YOLOv5**: ~83.3% mAP@0.5<br>- **Zero-DCE + YOLOv5**: ~85.6% mAP@0.5<br>- **Infrared Raw (Thermal)**: ~91.2% mAP@0.5<br>- **Multispectral Fusion**: **94.8% mAP@0.5** | - **TriFuse + YOLOv10**: **0.753 mAP(0.5)** / **0.692 mAP(0.5-0.9)**<br>- **SCI + YOLOv10**: 0.650 / 0.653<br>- **DiffLL + YOLOv10**: 0.650 / 0.568<br>- **LLFormer + YOLOv10**: 0.623 / 0.562 | - **DSFD Raw (No Enh)**: ~27.0% AP@0.5<br>- **Zero-DCE + DSFD**: ~32.4% AP@0.5<br>- **LIME + DSFD**: ~35.6% AP@0.5<br>- **HLA-Face (SOTA)**: **43.0% AP@0.5** |

---

> [!NOTE]
> **Nhận xét quan trọng về các tập dữ liệu hạ nguồn:**
> Các tập dữ liệu thuộc Nhánh 5 đánh dấu một sự chuyển dịch tư duy quan trọng trong cộng đồng LLIE: **từ "phục vụ thị giác người dùng" sang "phục vụ máy học"**. 
> - **ExDark** là benchmark kinh điển mở đường cho phát hiện vật thể đa lớp ban đêm, nhưng thiếu ảnh cặp tương ứng khiến việc huấn luyện giám sát LLIE gặp khó khăn.
> - **LLVIP** giải quyết triệt để vấn đề này cho đối tượng người đi bộ nhờ camera hồng ngoại nhiệt làm dẫn đường ánh xạ pixel.
> - **LoLI-Street** là đại diện SOTA mới nhất (ACCV 2024), cung cấp nguồn dữ liệu cặp siêu lớn về giao thông đô thị, thiết lập một chuẩn so sánh hiệu năng downstream (mAP của YOLOv10) vô cùng thực tế cho xe tự hành.
> - **DARK FACE** đại diện cho độ khó cực đoan nhất, nơi các thuật toán tăng sáng truyền thống thường bị sụp đổ hiệu năng do nhiễu hạt che lấp toàn bộ chi tiết cấu trúc khuôn mặt.
