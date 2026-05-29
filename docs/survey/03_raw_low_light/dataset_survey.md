# Khảo Sát Chi Tiết Các Bộ Dữ Liệu RAW Low-Light (SID, SDSD, SMID)

RAW Low-Light Enhancement là một nhánh nghiên cứu đặc thù và có tính học thuật cao trong bài toán Tăng cường ảnh thiếu sáng (LLIE). Thay vì xử lý trên ảnh đã qua bộ nén sRGB (như JPEG) vốn đã bị mất mát nhiều thông tin ánh sáng vật lý và bị biến dạng nhiễu do thuật toán phần cứng (ISP), các phương pháp RAW xử lý trực tiếp tín hiệu số thô từ cảm biến. Tài liệu này cung cấp bảng khảo sát chi tiết hệ thống ba bộ dữ liệu nền tảng nhất của nhánh này bao gồm: **SID (See-in-the-Dark)**, **SDSD (Static and Dynamic Scene Dataset)**, và **SMID (Seeing Motion in the Dark)**.

---

## 📊 Bảng 1: Thông Tin Cơ Bản (Basic Information)

Bảng này cung cấp cái nhìn tổng quan về nguồn gốc, quy mô, định dạng dữ liệu và mục đích thiết kế của từng bộ dữ liệu.

| Tiêu Chí Đánh Giá | See-in-the-Dark (SID) | Static and Dynamic Scene Dataset (SDSD) | Seeing Motion in the Dark (SMID) |
| :--- | :--- | :--- | :--- |
| **Tác giả & Năm công bố** | Chen Chen et al. (CVPR 2018) | Ruixing Wang et al. (ICCV 2021) | Chen Chen et al. (ICCV 2019) |
| **Loại dữ liệu (Data Type)** | RAW (Bayer & X-Trans) | sRGB (PNG) & RAW (tùy phiên bản chuyển đổi) | RAW (Bayer) |
| **Quy mô mẫu (Quantity)** | 5.094 cặp ảnh RAW phơi sáng ngắn và phơi sáng dài (tương ứng 424 cảnh tĩnh). | 150 chuỗi video cặp (70 trong nhà, 80 ngoài trời). Mỗi chuỗi dài từ 100 - 300 frames. | 21.839 frames ảnh RAW phơi sáng ngắn + ảnh tĩnh tham chiếu phơi sáng dài. |
| **Cấu trúc cặp (Paired/Unpaired)** | Paired (Được căn chỉnh pixel chính xác) | Paired (Được căn chỉnh không gian - thời gian nhờ hệ thống cơ điện tử) | Paired (Cảnh tĩnh có GT phơi sáng dài; cảnh động không có GT) |
| **Bối cảnh miền (Domain/Context)** | Cảnh tĩnh hoàn toàn, trong nhà và ngoài trời, điều kiện tối cực đoan. | Cảnh tĩnh và động (người đi bộ, xe cộ), trong nhà/ngoài trời với chuyển động camera được kiểm soát. | Cảnh động thực tế ngoài trời trong đêm, chuyển động của vật thể và camera thực tế. |
| **Độ phân giải (Resolution)** | - Sony Subset: $4240 \times 2832$<br>- Fuji Subset: $6000 \times 4000$ | $1920 \times 1080$ (sRGB gốc) hoặc $960 \times 512$ (npy rút gọn để huấn luyện nhanh) | $5496 \times 3672$ (RAW Bayer) |
| **Phân chia dữ liệu (Train/Val/Test)** | - Sony: 161 cảnh train, 36 val, 93 test.<br>- Fuji: 85 cảnh train, 12 val, 44 test. | 120 chuỗi video cho huấn luyện (Train), 30 chuỗi video cho kiểm thử (Test). | 151 chuỗi video cho huấn luyện, 27 chuỗi cho xác thực, 30 chuỗi cho kiểm thử. |
| **Nguồn tải & Giấy phép** | [SeeInTheDark](https://cchen156.github.io/SeeInTheDark.html) (Academic Only) | [SDSD GitHub](https://github.com/flyywh/Awesome-Low-Light-Enhancement) (Academic Only) | [SMID GitHub](https://github.com/cchen156/Seeing-Motion-in-the-Dark) (Academic Only) |

---

## ⚙️ Bảng 2: Đặc Tính Kỹ Thuật (Technical Characteristics)

Bảng này đi sâu vào khía cạnh phần cứng cảm biến, cấu hình thiết lập khi thu thập dữ liệu và các thách thức đặc thù về nhiễu vật lý của mỗi dataset.

| Đặc Tính Kỹ Thuật | See-in-the-Dark (SID) | Static and Dynamic Scene Dataset (SDSD) | Seeing Motion in the Dark (SMID) |
| :--- | :--- | :--- | :--- |
| **Cảm biến & Thiết bị chụp** | - Sony $\alpha7$S II (Bayer, Sony IMX235)<br>- Fujifilm X-T2 (X-Trans III) | Hệ thống cơ điện tử kết hợp camera công nghiệp Sony DSLR để chụp đồng thời hoặc tuần tự căn chỉnh. | Sony RX100 VI (Cảm biến Bayer kích thước 1-inch). |
| **Thiết lập ISO** | Cực cao: Từ ISO 800, 1600 đến tối đa **ISO 25600** (Sony) và **ISO 12800** (Fuji). | Kiểm soát linh hoạt: Từ ISO 800 đến ISO 6400 tùy thuộc vào cảnh. | High ISO: Thường thiết lập từ ISO 3200 đến **ISO 12800** để đảm bảo tốc độ màn trập. |
| **Thời gian & Tỷ lệ phơi sáng** | - Đầu vào: 1/30s hoặc 1/10s (cực tối)<br>- Ground Truth: 10s hoặc 30s<br>- Tỷ lệ khuếch đại: **1:100 đến 1:300** | Phơi sáng ngắn kết hợp bộ lọc ND để thu nhận đồng thời. Tỷ lệ khuếch đại dao động từ **1:10 đến 1:100**. | - Đầu vào: 1/30s đến 1/10s (tốc độ video thực tế)<br>- GT (chỉ cho cảnh tĩnh): 10s đến 30s<br>- Tỷ lệ: **1:120 đến 1:300** |
| **Định dạng file & Bit-depth** | - Sony: `.ARW` (14-bit RAW Bayer)<br>- Fuji: `.RAF` (14-bit RAW X-Trans) | `.png` (8-bit sRGB tiêu chuẩn) hoặc `.npy` (float32 được chuẩn hóa) | `.DNG` (12-bit RAW Bayer của Sony RX100 VI) |
| **Đặc điểm nhiễu (Noise)** | Nhiễu đọc (read noise) cực lớn, nhiễu hạt photon (shot noise) nặng, xuất hiện nhiều điểm ảnh chết (dead pixels/hot pixels). | Nhiễu nén sRGB, nhiễu thời gian phi tuyến tính, nhiễu chuyển động mờ (motion blur). | Hỗn hợp cực đoan: Nhiễu cảm biến RAW phơi sáng ngắn + Nhiễu động sinh ra do chuyển động của vật thể. |
| **Thách thức cốt lõi** | Khôi phục màu sắc chính xác từ tín hiệu cực yếu, triệt tiêu nhiễu sọc (stripe noise), khử nhiễu mà không làm bệt chi tiết. | Đồng bộ hóa chuyển động camera giữa hai luồng chụp phơi sáng khác nhau, duy trì tính nhất quán thời gian (temporal consistency). | Xử lý các khung hình động có nhiễu cực nặng và mờ nhòe do chuyển động mà không có Ground Truth tương ứng cho từng frame động. |

---

## 🔬 Bảng 3: Protocol & Đánh Giá (Protocol & Evaluation)

Bảng này phân tích các bước xử lý dữ liệu trước khi đưa vào mạng huấn luyện, các siêu tham số tiêu chuẩn và quy trình đánh giá kết quả.

| Tiêu Chí Quy Trình | See-in-the-Dark (SID) | Static and Dynamic Scene Dataset (SDSD) | Seeing Motion in the Dark (SMID) |
| :--- | :--- | :--- | :--- |
| **Pipeline tiền xử lý RAW** | **Pack RAW**: Chia Bayer Pattern ($H \times W \times 1$) thành 4 kênh ($H/2 \times W/2 \times 4$ đại diện cho R, Gr, Gb, B), trừ đi mức đen cảm biến (black level), sau đó nhân với hệ số khuếch đại mong muốn trước khi đưa vào mạng. | Xử lý trực tiếp trên định dạng RGB đã qua ISP hoặc sử dụng trực tiếp các file `.npy` đã được tiền xử lý và cắt (crop). | Đọc định dạng `.DNG` qua thư viện rawpy, thực hiện **Pack RAW** thành 4 kênh, khử mức đen cảm biến, nhân hệ số phơi sáng tương ứng của cảnh. |
| **Siêu tham số huấn luyện chuẩn** | - Optimizer: Adam<br>- Learning Rate: $10^{-4}$ (giảm dần về $10^{-5}$)<br>- Batch Size: 1<br>- Patch Size: $512 \times 512$ (RAW patch, tương đương $1024 \times 1024$ RGB) | - Optimizer: Adam<br>- Learning Rate: $10^{-4}$<br>- Batch Size: 4 hoặc 8<br>- Patch Size: $256 \times 256$ hoặc $512 \times 512$ sRGB | - Optimizer: Adam<br>- Learning Rate: $10^{-4}$<br>- Batch Size: 1 (do giới hạn VRAM GPU với chuỗi video RAW)<br>- Patch Size: $256 \times 256$ (RAW) |
| **Chỉ số đánh giá chính** | **PSNR**, **SSIM** (tính trên ảnh sRGB đầu ra sau khi qua thuật toán demosaic tiêu chuẩn như LibRaw/dcraw), kết hợp **LPIPS**. | **PSNR**, **SSIM** phục hồi sRGB, kết hợp chỉ số nhất quán thời gian **tOF (temporal Optical Flow error)**. | **PSNR**, **SSIM**, **LPIPS** cho các khung hình tĩnh; kiểm thử thị giác người dùng (User Study) và **NIQE** cho video động. |
| **Vấn đề căn chỉnh (Alignment)** | Dù là cảnh tĩnh, sự rung động nhỏ của gió hoặc chân máy vẫn có thể gây lệch sub-pixel. Phải căn chỉnh dịch chuyển (sub-pixel shift) trước khi tính loss. | Sử dụng căn chỉnh cơ học bằng robot chụp kết hợp căn chỉnh quang học (Optical Flow alignment) để loại bỏ sai lệch động. | Cảnh tĩnh được căn chỉnh tốt bằng chân máy. Cảnh động hoàn toàn không có Ground Truth ở cấp độ pixel cho từng frame, chỉ có GT ở cấp độ ngữ cảnh tĩnh. |
| **Đầu ra mong muốn (Target)** | Ảnh sRGB chất lượng cao sau khi đã khôi phục màu, khử nhiễu và tăng sáng tương đương ảnh phơi sáng dài. | Video sRGB mượt mà, sáng rõ, không có hiện tượng nhấp nháy (flicker) và giữ được chi tiết biên. | Video RAW hoặc video sRGB đã khử nhiễu cực đoan và khôi phục mượt mà các chi tiết chuyển động trong đêm. |
