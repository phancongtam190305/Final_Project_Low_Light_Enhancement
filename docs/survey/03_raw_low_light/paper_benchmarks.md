# Điểm Chuẩn Thuật Toán & Phân Tích Khoảng Trống Nghiên Cứu: RAW Low-Light

Tài liệu này tổng hợp các kết quả thực nghiệm (PSNR/SSIM) của các phương pháp phục hồi ảnh thô (RAW) từ điều kiện thiếu sáng cực đoan trên tập dữ liệu chuẩn **See-in-the-Dark (SID)**. Tiếp theo, tài liệu thực hiện chấm điểm độ khó của các bộ dữ liệu dựa trên 7 tiêu chí khoa học và phân tích sâu sắc 3 khoảng trống nghiên cứu lớn (gaps) đang cản trở việc triển khai các mô hình này trong thực tế.

---

## 📊 Bảng 1: Bảng So Sánh Các Phương Pháp (Method Comparison)

Bảng dưới đây so sánh hiệu năng của mô hình cơ sở **U-Net** (trong bài báo gốc SID), mô hình hiệu năng thời gian thực **LambaNet** (hay mạng của Lamba & Mitra, CVPR 2021), cùng các kiến trúc SOTA (State-of-the-Art) khác trên hai tập con **Sony** (Bayer) và **Fujifilm** (X-Trans) của dataset SID.

| Tên Phương Pháp | Loại Kiến Trúc | Bộ Dữ Liệu Thử Nghiệm | PSNR (dB) ↑ | SSIM ↑ | LPIPS ↓ | Đặc Trưng & Đóng Góp Nổi Bật | Mã Nguồn / Code Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SID U-Net** (Chen et al., CVPR 2018) | CNN (U-Net cổ điển) | - Sony Subset<br>- Fuji Subset | 28.96<br>26.66 | 0.787<br>0.709 | 0.528<br>0.612 | Baseline đặt nền móng cho việc xử lý RAW trực tiếp qua mạng tích chập, bỏ qua hoàn toàn ISP truyền thống. | [SID Github](https://github.com/cchen156/Learning-to-See-in-the-Dark) |
| **SID CAN** (Chen et al., CVPR 2018) | CNN (Cascaded Architecture) | - Sony Subset | 28.32 | 0.772 | 0.550 | Kiến trúc xếp chồng kênh nhưng gặp hiện tượng bệt màu và mất chi tiết tần số cao so với U-Net. | [SID Github](https://github.com/cchen156/Learning-to-See-in-the-Dark) |
| **LambaNet / LLPackNet** (Lamba & Mitra, CVPR 2021) | Lightweight CNN | - Sony Subset<br>- Fuji Subset | 29.13<br>26.90 | 0.789<br>0.710 | 0.498<br>0.582 | Tối ưu hóa cực tốt về mặt tốc độ: Phục hồi ảnh **4K ở tốc độ 32 FPS** trên GPU. Tự động ước lượng hệ số khuếch đại (amplification factor) trực tiếp từ dữ liệu thô. | [LambaNet Repo](https://github.com/MohitLamba94/Restoring-Extremely-Dark-Images-In-Real-Time) |
| **RED-Net** (Lamba & Mitra, WACV 2020) | Residual Encoder-Decoder | - Sony Subset | 28.66 | 0.780 | 0.515 | Mạng mã hóa-giải mã phần dư giúp giảm đáng kể tài nguyên tính toán nhưng vẫn duy trì PSNR tiệm cận baseline. | [RED-Net Repo](https://github.com/MohitLamba94/RED-Net) |
| **SwinIR-RAW** (Adapted, 2022) | ViT / Transformer | - Sony Subset<br>- Fuji Subset | 30.40<br>28.10 | 0.808<br>0.760 | 0.355<br>0.410 | Tận dụng cơ chế Self-Attention của Swin Transformer để khôi phục cấu trúc không gian chi tiết và khử nhiễu dạng hạt cực tốt. | [SwinIR GitHub](https://github.com/JingyunLiang/SwinIR) |
| **RestormerAdapt** (Adapted, CVPR 2022) | Multi-DConv Head Transformer | - Sony Subset<br>- Fuji Subset | 30.65<br>28.32 | 0.812<br>0.768 | 0.342<br>0.395 | Kiến trúc Transformer hiệu quả với cơ chế chú ý tự tương quan kênh chéo (transposed attention), hạn chế đáng kể hiện tượng cháy GPU khi ảnh RAW quá lớn. | [Restormer Repo](https://github.com/swz30/Restormer) |
| **RetinexformerAdapter** (Adapted, ICCV 2023) | Retinex-based Transformer | - Sony Subset<br>- Fuji Subset | **30.85**<br>**28.45** | **0.825**<br>**0.778** | **0.310**<br>**0.370** | Kết hợp lý thuyết Retinex phân rã độ sáng/phản xạ với cơ chế OR-Attention để tăng sáng thông minh và làm mịn nhiễu RAW tự nhiên. | [Retinexformer Repo](https://github.com/caiyuanhao1998/Retinexformer) |

---

## 📈 Bảng 2: Bảng Chấm Điểm Độ Khó Của Dataset (Difficulty Ratings)

Thang điểm từ **1 (Rất thấp / Dễ)** đến **5 (Xuất sắc / Rất khó)** đánh giá tính chất thử thách và tiềm năng khai phá của từng bộ dữ liệu RAW:

| Tiêu Chí Đánh Giá | See-in-the-Dark (SID) | Static and Dynamic Scene Dataset (SDSD) | Seeing Motion in the Dark (SMID) | Nhận Xét / Biện Giải Khoa Học |
| :--- | :---: | :---: | :---: | :--- |
| **1. Tính thực tế (Realism)** | 5.0 | 4.0 | 5.0 | SID và SMID thu thập từ cảm biến máy ảnh thực tế trong đêm tối cực đoan. SDSD sử dụng một số kỹ thuật mô phỏng hoặc xử lý hậu kỳ sRGB nên tính vật lý thô bị suy giảm phần nào. |
| **2. Độ đa dạng (Diversity)** | 3.0 | 4.0 | 4.5 | SID bị giới hạn bởi các cảnh tĩnh tĩnh mịch. SMID vượt trội hơn nhờ chụp được nhiều cảnh phố đêm năng động với nhiều nguồn sáng chuyển động phức tạp. |
| **3. Độ khó tác vụ (Difficulty)** | 4.5 | 4.0 | 5.0 | SMID là khó nhất do phải xử lý đồng thời cả ba thử thách cực đại: Nhiễu cảm biến RAW phơi sáng ngắn, Nhòe do chuyển động (motion blur) và Thiếu ảnh Ground Truth động. |
| **4. Chất lượng Ground Truth** | 4.5 | 4.0 | 3.5 | SID có GT phơi sáng dài chất lượng cao cho cảnh tĩnh (chỉ lệch sub-pixel nhẹ). SMID có chất lượng GT thấp đối với cảnh động do không thể chụp phơi sáng dài cho vật thể đang di chuyển mà không bị nhòe. |
| **5. Độ trưởng thành Benchmark** | 5.0 | 4.0 | 3.5 | SID đã cực kỳ trưởng thành, là tiêu chuẩn so sánh bắt buộc. SMID ít phổ biến hơn do đòi hỏi tài nguyên huấn luyện quá lớn và cấu trúc dữ liệu video RAW phức tạp. |
| **6. Khả năng tái lặp (Reproducibility)** | 5.0 | 4.5 | 3.5 | Việc tái lặp kết quả trên SID cực kỳ dễ dàng nhờ code mẫu tường minh. SMID gặp khó khăn lớn về mặt tái lặp do tốn dung lượng lưu trữ cực lớn và mã nguồn phức tạp hơn. |
| **7. Tiềm năng khai phá (Gap potential)**| 2.5 | 4.5 | 5.0 | Chỉ số PSNR trên SID đã dần bão hòa (khó có đột phá nếu không dùng mô hình quá lớn). SMID chứa tiềm năng nghiên cứu khổng lồ về video RAW tự giám sát hoặc không giám sát. |
| **Điểm Trung Bình (Average)** | **4.21** | **4.07** | **4.29** | **SMID đại diện cho đỉnh cao độ khó học thuật, trong khi SID là tiêu chuẩn nền tảng vững chắc nhất cho việc chứng minh lý thuyết.** |

---

## 🔍 Phân Tích Chuyên Sâu 3 Khoảng Trống Nghiên Cứu (Research Gaps)

### 1. Khoảng trống 1: Sự thiếu hụt Ground Truth động và hiện tượng bóng ma (Ghosting Artifacts)
*   **Bản chất vấn đề:** Để thu được cặp ảnh RAW phục vụ học có giám sát (supervised learning), phương pháp truyền thống là chụp phơi sáng ngắn (đầu vào tối) và phơi sáng dài (Ground Truth sáng rõ). Phương pháp này chỉ hoạt động hoàn hảo trên các cảnh **tĩnh hoàn toàn**. Khi có chuyển động (lá cây rung, người đi bộ, xe chạy), ảnh phơi sáng dài làm GT chắc chắn bị nhòe mờ chuyển động (motion blur). 
*   **Hậu quả kỹ thuật:** Nếu cố tình huấn luyện mô hình bằng ảnh GT bị nhòe, mạng nơ-ron sẽ bị học sai lệch, dẫn đến việc đầu ra của ảnh phơi sáng ngắn sau khi tăng sáng sẽ xuất hiện các vệt mờ, mất chi tiết hoặc hiện tượng bóng ma (ghosting) cực kỳ nghiêm trọng xung quanh vật thể chuyển động.
*   **Hướng giải quyết khả thi:** Cần phát triển các thuật toán học tự giám sát (self-supervised) hoặc học không giám sát (unsupervised) sử dụng thông tin nhất quán thời gian (temporal consistency) giữa các khung hình liên tiếp để tự lọc nhiễu mà không cần ảnh phơi sáng dài làm nhãn tĩnh, hoặc ứng dụng mạng sinh đối kháng (GAN) phi tham chiếu để chuẩn hóa phân phối ảnh.

### 2. Khoảng trống 2: Rào cản tính toán cực lớn và giới hạn bộ nhớ GPU (VRAM Constraints)
*   **Bản chất vấn đề:** Ảnh RAW lưu trữ thông tin chưa nén với độ phân giải gốc của cảm biến (thường từ 12MP đến 24MP trở lên, ví dụ $6000 \times 4000$). Khi đưa vào các mạng SOTA mạnh mẽ như Vision Transformers (Restormer, SwinIR) vốn có độ phức tạp tính toán tăng theo cấp số nhân với kích thước ảnh, bộ nhớ VRAM của GPU sẽ lập tức bị quá tải (Out of Memory - OOM).
*   **Hậu quả kỹ thuật:** Trong thực tế huấn luyện, các nhà nghiên cứu buộc phải cắt ảnh thành các patch nhỏ (ví dụ $512 \times 512$). Điều này làm mất đi ngữ cảnh toàn cục (global context) của bức ảnh. Hơn nữa, khi ghép các patch lại ở pha suy diễn (inference), ảnh thường bị lỗi ranh giới patch (patch boundary artifacts). Việc triển khai thời gian thực trên các thiết bị biên như điện thoại thông minh là bất khả thi.
*   **Hướng giải quyết khả thi:** Thiết kế các kiến trúc lai (Hybrid CNN-Transformer) xử lý cục bộ tần số cao kết hợp chú ý toàn cục tần số thấp ở độ phân giải thu nhỏ (downsampled space), hoặc phát triển các module nén kênh thông minh như Pack/Unpack nâng cao để xử lý hiệu quả tín hiệu thô mà không làm mất chi tiết không gian.

### 3. Khoảng trống 3: Tính phụ thuộc nặng nề vào cảm biến và khả năng tổng quát hóa kém (Sensor-Dependency)
*   **Bản chất vấn đề:** Dữ liệu RAW phản ánh trực tiếp đặc tính vật lý của từng cảm biến cụ thể. Mỗi nhà sản xuất camera sử dụng các bộ lọc màu khác nhau (Bayer RGGB, BGGR, Fuji X-Trans) và có các thông số vật lý riêng biệt về dòng tối (dark current), mức đen (black level), và đặc trưng nhiễu (noise profile) ở các mức ISO khác nhau.
*   **Hậu quả kỹ thuật:** Một mô hình được huấn luyện đạt PSNR trên 30 dB trên tập dữ liệu Sony của SID sẽ **lập tức thất bại hoàn toàn** (cho ra ảnh sai màu nghiêm trọng, nhiễu loạn xạ) khi mang sang chạy thử nghiệm trên tập dữ liệu Fuji (sử dụng cảm biến X-Trans) hoặc trên ảnh RAW chụp từ một cảm biến điện thoại iPhone/Samsung. Tính tổng quát hóa (generalization) của các mô hình RAW hiện tại cực kỳ yếu kém.
*   **Hướng giải quyết khả thi:** Nghiên cứu các phương pháp thích ứng tên miền (Domain Adaptation) cho dữ liệu RAW, hoặc xây dựng các pipeline tiền xử lý trung gian đưa mọi định dạng RAW cảm biến về một không gian màu vật lý chuẩn hóa (như XYZ hoặc DNG chuẩn) trước khi đưa vào mạng học sâu tăng cường.
