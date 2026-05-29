# Kế Hoạch Khảo Sát Đề Tài Tốt Nghiệp: Low Light Enhancement

Tài liệu này ghi nhận kế hoạch khảo sát chi tiết cho đồ án tốt nghiệp Low-Light Image Enhancement (LLIE).

---

## 🎯 Mục Tiêu Đầu Ra
Sau khi hoàn thành phần khảo sát này, bạn sẽ đạt được **4 sản phẩm** cốt lõi:
1. **Bảng tổng hợp dataset LLIE**: Tên, link, loại data, số lượng, paired/unpaired, domain, resolution, train/test split, license.
2. **Bảng "Ai đã dùng dataset đó và dùng như thế nào"**: Paper, method, supervised/unsupervised/zero-shot, train/test protocol, metric.
3. **Bảng Gap Analysis**: Dataset nào đã bão hòa, dataset nào còn thiếu benchmark, các vấn đề còn mở (open problems).
4. **Đề xuất hướng đồ án**: Chọn 1–2 dataset chính + 1–2 dataset để kiểm tra khả năng tổng quát hóa (generalization).

---

## 📋 Lộ Trình Chi Tiết Từng Bước

### **Bước 1: Chốt phạm vi bài toán**
* Phân loại LLIE thành các nhánh (Paired, Unpaired, RAW, Real-world high-res, Downstream tasks).
* Đọc và ghi rõ đồ án của bạn thuộc loại nào: *Image enhancement thuần túy* hay *Enhancement phục vụ downstream task* (detection / recognition).

### **Bước 2: Lập danh sách dataset nền tảng**
* Ưu tiên khảo sát các dataset chủ lực: LOL v1, LOL-v2 (Real/Synthetic), SID, SICE, DICM/LIME/NPE/MEF, ExDark, LLVIP, LoLI-Street, NTIRE (2024/2025).

### **Bước 3: Tạo template khảo sát dataset**
* Tạo cấu trúc bảng thu thập thông tin cơ bản, đặc tính kỹ thuật, và evaluation protocol của từng dataset.

### **Bước 4: Khảo sát các nghiên cứu đi trước ("Ai đã làm và làm như thế nào")**
* Tìm kiếm các nghiên cứu tiêu biểu ứng với từng dataset (RetinexNet, Zero-DCE, KinD, MIRNet, SNR-Aware, Retinexformer, NTIRE teams...).
* Ghi lại chi tiết: Paper, năm, dataset dùng, phương pháp giám sát, metrics, mã nguồn.

### **Bước 5: Đánh giá độ khó / dễ của các dataset**
* Chấm điểm từng dataset theo thang 1–5 dựa trên các tiêu chí: Realism, Diversity, Difficulty, Ground truth quality, Benchmark maturity, Reproducibility, Gap potential.

### **Bước 6: Phân tích khoảng trống nghiên cứu (Gap Analysis)**
* Tìm kiếm và lập luận các khoảng trống thực tế (khả năng generalization kém, quá phụ thuộc vào paired data, xử lý nhiễu kết hợp, non-uniform illumination, high-resolution, downstream tasks, edge deployment...).

### **Bước 7: Đề xuất chiến lược dataset cho đồ án**
* Lựa chọn 1 trong các hướng đi chiến lược (Option A: An toàn/Dễ, Option B: Có chiều sâu, Option C: Nghiên cứu khó/RAW, Option D: Có tính mới/NTIRE).

### **Bước 8: Checklist nghiệm thu nhiệm vụ khảo sát**
* [ ] Có bảng so sánh ít nhất 10 dataset LLIE kèm link download.
* [ ] Có thông tin chi tiết cấu trúc (paired, split, resolution...) cho mỗi dataset.
* [ ] Khảo sát ít nhất 3–5 paper tiêu biểu cho mỗi dataset.
* [ ] Có bảng so sánh metric và protocol huấn luyện.
* [ ] Có phân tích nhận xét các dataset đã bão hòa và chỉ ra ít nhất 5 khoảng trống nghiên cứu (gaps).
* [ ] Có đề xuất chiến lược lựa chọn dataset rõ ràng cho đồ án và kế hoạch thí nghiệm sơ bộ.
