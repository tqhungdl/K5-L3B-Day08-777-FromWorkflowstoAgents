# Phần báo cáo nhóm — Đặng Nhật Huy (2A202603822) — Shape B (single agent)

---

## Copy vào mục 3 "Giải pháp" của group_report.md

Shape B (`src/lab8/shapes/single.py`) là một vòng ReAct, giới hạn 8 bước qua `lab8.runtime.run_react`. Hàm `decide` chỉ chọn tool đọc: `lookup_order` rồi `compute_compensation` trên dòng order lấy từ DB. Hàm này không đọc nội dung ticket, nên số ngày trễ người dùng ghi trong ticket không ảnh hưởng đến số tiền. Mỗi bước gọi `complete()` để ghi vào Budget, giúp chi phí so sánh được với các shape khác.

Ranh giới code và model: `decide` chỉ chọn tool đọc. Số tiền do `compute_compensation` tính. Shape truyền **quote đầy đủ** vào `durability.issue_refund`; host tự trừ phần đã hoàn trước đó và kiểm approval. Shape không tự ghi ledger.

Trace ghi các event đã qua allowlist: kết quả `lookup_order` đã lọc, quote, quyết định, kết quả host. Shape không ghi nội dung ticket và không ghi nguyên claim row hay order row. Khi crash được chỉ định (`crash_at`), trace được ghi trước khi `InjectedCrash` được ném lên caller.

---

## Copy vào mục 4 "Kết quả" của group_report.md

Không chép số từ bảng này vào báo cáo nhóm. Số chính thức lấy từ `src/reports/benchmark.json` và `src/reports/crash.json` do lệnh của lab tạo ra.

Kết quả kiểm tra của shape B trong quá trình phát triển (tham khảo, không thay thế số trong file report):
- Test student `-k single` cho shape B: 62 passed.
- Test riêng `src/tests/test_single_shape.py`: 20 passed.

---

## Copy vào mục 5 "Khó khăn và cách xử lý" của group_report.md

- **Môi trường Python:** máy chỉ có Python 3.14, README ghi 3.11–3.13. Tạo venv bằng `py -3 -m venv .venv` rồi cài `requirements.txt` vẫn chạy được pytest và smoke test. Cần kiểm tra lại trên máy khác nếu có lỗi.
- **Chạy test có filter `-k`:** `-k single` khớp cả tên hàm test dùng chung nên chạy cả shape workflow và orchestrator (đang là stub). Cách xử lý: lọc bằng `-k "single and not workflow and not orchestrator and not swarm"`.

---

## Copy vào mục 6 "Tổng hợp đóng góp" (tham khảo, bảng chính nằm trong TEAM.md)

- Đặng Nhật Huy (2A202603822): shape B `src/lab8/shapes/single.py`; test `src/tests/test_single_shape.py` (5 nhóm test). Commit hash: 0970390.
