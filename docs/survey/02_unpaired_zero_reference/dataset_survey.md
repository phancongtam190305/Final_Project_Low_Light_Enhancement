# Khảo Sát Tập Dữ Liệu Nhánh 2: Unpaired / Zero-Reference

Tài liệu này thực hiện khảo sát chi tiết và hệ thống hóa thông tin khoa học của các tập dữ liệu không cặp (unpaired datasets) phổ biến nhất được sử dụng để đánh giá khả năng tổng quát hóa và hiệu năng thực tế của các mô hình trong nhánh nghiên cứu **Unpaired / Zero-Reference Low-Light Image Enhancement**. Các tập dữ liệu bao gồm: **DICM**, **LIME**, **MEF** và **NPE**.

---

## 1. Bảng 1: Thông Tin Cơ Bản (Basic Information)

Bảng này cung cấp thông tin nguồn gốc học thuật, quy mô và đặc trưng phân phối vật lý cơ bản của các tập dữ liệu.

| Tiêu Chí | DICM | LIME | MEF | NPE |
| :--- | :--- | :--- | :--- | :--- |
| **Năm công bố** | 2012 | 2016 | 2015 | 2013 |
| **Hội nghị / Tạp chí** | IEEE Transactions on Consumer Electronics | IEEE Transactions on Image Processing (TIP) | IEEE Transactions on Image Processing (TIP) | IEEE Transactions on Image Processing (TIP) |
| **Nhóm tác giả / Đơn vị** | Chulwoo Lee, Chul-Woo Kim, Chang-Su Kim <br>*(Korea University)* | Xiaojie Guo, Yu Li, Haibin Ling <br>*(Temple University & Lenovo)* | K. Ma et al. <br>*(University of Waterloo)* | Shuhang Wang et al. <br>*(Tsinghua University)* |
| **Link download chính thức** | [DICM Download](https://github.com/Li-Chongyi/Zero-DCE) *(Tích hợp trong Zero-DCE)* | [LIME Project Page](https://github.com/weichen582/LIME) | [MEF Download](https://github.com/Li-Chongyi/Zero-DCE) *(Tích hợp trong Zero-DCE)* | [NPE Project Page](https://github.com/Li-Chongyi/Zero-DCE) *(Tích hợp trong Zero-DCE)* |
| **Số lượng ảnh** | 69 ảnh thiếu sáng đơn lẻ | 10 ảnh thiếu sáng chất lượng cao | 17 ảnh đa phơi sáng tiêu biểu | 85 ảnh thiếu sáng thực tế |
| **Loại cấu trúc** | **Unpaired** (Không có ảnh cặp Ground Truth) | **Unpaired** (Không có ảnh cặp Ground Truth) | **Unpaired** (Không có ảnh cặp Ground Truth) | **Unpaired** (Không có ảnh cặp Ground Truth) |
| **Phân chia Train / Test** | 0 Train / 69 Test <br>*(Thuần túy dùng để kiểm thử)* | 0 Train / 10 Test <br>*(Thuần túy dùng để kiểm thử)* | 0 Train / 17 Test <br>*(Thuần túy dùng để kiểm thử)* | 0 Train / 85 Test <br>*(Thuần túy dùng để kiểm thử)* |
| **Độ phân giải (Resolution)**| Đa dạng (từ ~300×400 đến 1200x900) | Cao (lên tới ~1000×800 trở lên) | Đa dạng (phổ biến xung quanh 500x300) | Đa dạng (thường từ 600x400 đến 1000x800) |
| **Định dạng dữ liệu** | sRGB (JPG, 8-bit) | sRGB (PNG & JPG, 8-bit) | sRGB (PNG & JPG, 8-bit) | sRGB (PNG & JPG, 8-bit) |
| **Bản quyền (License)** | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại | Sử dụng học thuật phi thương mại |

---

## 2. Bảng 2: Đặc Tính Kỹ Thuật (Technical Characteristics)

Bảng này phân tích cấu trúc vật lý của ảnh thiếu sáng, môi trường quang học khi chụp, mức độ phức tạp của độ phơi sáng và các kiểu nhiễu đặc trưng.

| Tiêu Chí Kỹ Thuật | DICM | LIME | MEF | NPE |
| :--- | :--- | :--- | :--- | :--- |
| **Nguồn gốc thiết bị chụp**| Thu thập từ nhiều loại máy ảnh kỹ thuật số (digital cameras) cầm tay khác nhau của người tiêu dùng. | Chụp thực tế bằng máy ảnh thương mại tại các địa điểm công cộng ban đêm. | Trích xuất từ bộ dữ liệu đa phơi sáng (Multi-Exposure Fusion dataset). | Chụp bằng các thiết bị khác nhau trong bối cảnh thực tế. |
| **Cơ chế chiếu sáng** | Thiếu sáng tự nhiên toàn cảnh hoặc ngược sáng nhẹ, độ sáng tương đối đồng đều nhưng phân bố tối sâu. | Độ tối rất sâu (deep low-light), chủ yếu là cảnh đêm đường phố có nguồn sáng điểm nhân tạo phức tạp. | Dải động rộng (HDR) với các mức độ phơi sáng cực đoan (tối gắt xen kẽ các vùng trung tính). | Ánh sáng phơi sáng cực kỳ không đồng đều (**Non-uniform illumination**), nhiều bóng râm sâu xen lẫn vùng nắng sáng. |
| **Sự hiện diện của Ground Truth**| **Hoàn toàn không có**. Mô hình tự phục hồi dựa trên các đặc trưng tự nhiên bất biến. | **Hoàn toàn không có**. Ảnh chỉ được tăng cường để kiểm thử độ tự nhiên về mặt thị giác. | **Hoàn toàn không có** đối với phiên bản LLIE (chỉ dùng ảnh tối nhất của chuỗi phơi sáng làm input). | **Hoàn toàn không có**. Thiết kế riêng để đánh giá sự bảo toàn tính tự nhiên của màu sắc. |
| **Mức độ Nhiễu (Noise & Artifacts)**| Trung bình. Nhiễu hạt cảm biến nhẹ kết hợp một số lỗi nén JPEG (compression artifacts). | Rất cao. Do chụp cảnh đêm thực tế phơi sáng ngắn, nhiễu hạt cảm biến xuất hiện rất rõ ở các góc tối sâu. | Thấp - Trung bình. Do được tuyển chọn kỹ từ tập HDR, ít bị nhiễu hạt nặng nhưng dễ bị nhòe chuyển động (motion blur). | Thấp. Ảnh chủ yếu tập trung vào độ tương phản không đồng đều hơn là nhiễu hạt cảm biến sâu. |
| **Độ đa dạng bối cảnh** | Cực kỳ cao. Gồm ảnh đời sống thường ngày, động vật (mèo, chim), con người, hoạt động ngoài trời, phong cảnh. | Trung bình. Tập trung vào cảnh phố xá ban đêm, công viên, biển hiệu neon, kiến trúc đô thị tối. | Cao. Bao gồm nội thất phòng ốc, phong cảnh thiên nhiên, kiến trúc ngoài trời với dải phơi sáng đa dạng. | Cực kỳ cao. Bối cảnh đa dạng gồm cả chụp ngược sáng ban ngày, bóng râm dưới tán cây, tòa nhà cổ. |
| **Độ tương phản và Dải động**| Trung bình. Các vùng tối phân bố mềm mại, dải động tương đối dễ phục hồi. | Rất thấp. Độ tương phản cực hạn ở các vùng bóng tối sâu, yêu cầu mô hình có khả năng kéo sáng mạnh. | Rất cao. Chứa cả vùng cháy sáng (bright sources) và tối sâu, dễ bị cháy sáng nếu tăng cường quá mức. | Phức tạp nhất. Dải động phi tuyến tính gắt do chênh lệch phơi sáng không đồng đều lớn giữa các vùng trong ảnh. |

---

## 3. Bảng 3: Giao thức huấn luyện & Đánh giá (Protocol & Evaluation)

Do không có ảnh Ground Truth để làm hệ quy chiếu trực tiếp, giao thức đánh giá của các tập dữ liệu này mang tính đặc thù cao, chủ yếu sử dụng các độ đo đánh giá phi tham chiếu (No-Reference Image Quality Assessment).

| Tiêu Chí Đánh Giá | DICM | LIME | MEF | NPE |
| :--- | :--- | :--- | :--- | :--- |
| **Giao thức huấn luyện** | **Không dùng để huấn luyện**. Chỉ đóng vai trò là tập Validation/Testing ngoại miền để kiểm thử khả năng Zero-Shot Generalization. | **Không dùng để huấn luyện**. Thuần túy dùng để kiểm thử độ ổn định thị giác trên các trường hợp thiếu sáng nghiêm trọng. | **Không dùng để huấn luyện**. Dùng làm tập kiểm thử độ bền bỉ dải động của thuật toán. | **Không dùng để huấn luyện**. Dùng làm tập kiểm thử độ bảo toàn màu sắc tự nhiên. |
| **Metrics đánh giá định lượng**| Sử dụng các chỉ số Chất lượng Ảnh Không Tham Chiếu: **NIQE** (Naturalness Image Quality Evaluator), **BRISQUE**, **PI** (Perceptual Index), và **LOE** (Lightness Order Error). | NIQE, BRISQUE, LOE, Entropy (đo lượng thông tin phục hồi). | NIQE, BRISQUE, LOE. | NIQE, LOE, chỉ số bảo toàn màu sắc CIEDE2000 (nếu có ước lượng gián tiếp). |
| **Phương pháp kiểm thử đặc thù** | Thường được chạy suy diễn (inference) trực tiếp từ mô hình đã pre-train trên LOL hoặc huấn luyện không giám sát trên tập dữ liệu khác (e.g. PART 1 của SICE hoặc các tập dữ liệu Unpaired lớn). | Đánh giá khả năng khôi phục cấu trúc viền sắc nét và kiểm soát quầng sáng quanh bóng đèn (halo artifacts control). | Đánh giá mức độ bảo toàn các chi tiết trong vùng sáng sáng (over-exposure control) đồng thời kéo sáng vùng tối. | Đánh giá độ tự nhiên thị giác thông qua việc so sánh thứ tự sáng tối cục bộ (**Lightness Order Error**) trước và sau nâng sáng. |
| **Đánh giá chủ quan (User Study)**| Cực kỳ quan trọng. Các nghiên cứu bắt buộc phải tiến hành khảo sát ý kiến người dùng trực quan (User Preference Scores) để chấm điểm thẩm mỹ. | Thường kết hợp so sánh visual với các phương pháp truyền thống như CLAHE, HE để kiểm chứng độ tự nhiên. | Khảo sát người dùng về độ dễ chịu khi quan sát dải tương phản cao, tránh hiện tượng giả tạo (unnatural look). | Đánh giá chủ quan xem ảnh có bị biến dạng màu sắc (color distortion) hay trông quá giả tạo hay không. |
| **Chỉ số Baseline tiêu biểu (NIQE)** | - **RetinexNet**: ~4.33 <br>- **Zero-DCE**: **~4.58** *(bảo toàn tự nhiên tốt)* <br>- **KinD**: **~3.95** *(đạt độ tự nhiên cao)* <br>- **EnlightenGAN**: ~4.06 | - **RetinexNet**: ~5.75 <br>- **Zero-DCE**: ~5.82 <br>- **KinD**: **~4.42** <br>- **EnlightenGAN**: ~4.59 | - **RetinexNet**: ~4.93 <br>- **Zero-DCE**: ~4.93 <br>- **KinD**: **~4.45** <br>- **EnlightenGAN**: ~4.70 | - **RetinexNet**: ~4.95 <br>- **Zero-DCE**: ~4.53 <br>- **KinD**: **~3.92** <br>- **EnlightenGAN**: ~3.99 |

---

> [!IMPORTANT]
> **Kết luận khảo sát Dataset Unpaired:**
> Do đặc thù hoàn toàn không có ảnh cặp Ground Truth chuẩn, nhóm bốn dataset **DICM, LIME, MEF, NPE** đóng vai trò là "liều thuốc thử cực mạnh" để đánh giá bản lĩnh thực tế của bất kỳ mô hình LLIE nào. Một mô hình có thể đạt PSNR cực cao trên LOL nhờ overfitting, nhưng sẽ dễ dàng bị phơi bày nhược điểm (nhiễu loang lổ, cháy sáng, lệch màu nghiêm trọng) khi chạy trên các tập dữ liệu kiểm thử thực tế này. Chỉ số **NIQE** (càng thấp càng tốt) và **LOE** (càng thấp càng tốt) là hai thước đo học thuật đáng tin cậy nhất để chấm điểm thuật toán tại đây.
