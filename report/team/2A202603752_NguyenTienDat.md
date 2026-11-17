# Báo cáo cá nhân — 2A202603752_NguyenTienDat

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tiến Đạt
- MSSV: 2A202603752
- Email: nguyentiendatqb126@gmail.com
- GitHub: chesschillchill

## 2. Phần việc phụ trách

Shape A — workflow trong `src/lab8/shapes/workflow.py`, phạm vi CP2–CP4.

## 3. Đóng góp cụ thể

- Commit: `4ca802c` — `feat: CP2 and CP3 for workflow shape`.
- Commit CP4: `b389b75` — `test: add workflow safety checks`.
- CP2: đọc claim bằng `get_claim_view`, kiểm tra order và quyền sở hữu qua `lookup_order`, tính quote bằng `compute_compensation` từ dữ liệu database. Không dùng nội dung ticket để quyết định số tiền.
- Quote dương được truyền đầy đủ vào `issue_refund`; host kiểm approval, giới hạn số tiền và trừ phần đã hoàn. Workflow không tự ghi ledger.
- CP3: truyền `crash_at` vào `issue_refund`, không bắt `InjectedCrash`; đóng kết nối bằng `finally`.
- Dùng `finish()` để trả `RunResult` và ghi trace ở các nhánh kết thúc bình thường. Trace chỉ ghi order view đã lọc, quote và quyết định; không ghi ticket hoặc nguyên claim row.
- Workflow không gọi MockLLM. Budget ghi nhận các lời gọi tool.
- CP4: thêm `src/tests/test_workflow_safety.py` (11 test) kiểm tra approval, trace/stdout và phục hồi ở ba vị trí crash. Chạy crash suite tạo `src/reports/crash.json`.

## 4. Bằng chứng

Kiểm tra tại commit `4ca802c`, chạy trong `src/`:

```bash
python -m pytest -q -m student -o addopts= -k workflow
# 62 passed, 260 deselected

python -m pytest -q
# 74 passed, 248 deselected
```

Test workflow gồm T11 (`test_t11_retry_keeps_one_refund`) và T12 (`test_t12_crash_before_checkpoint_does_not_double_pay`). Cả hai đã pass: chạy lại và crash rồi resume vẫn giữ một refund và một audit `refund_committed`.

Kết quả CP4, commit `b389b75`: test riêng 11 passed; test student workflow 62 passed; bộ test mặc định 85 passed. Lệnh `python -m lab8.crash_test --count 20 --out reports/crash.json` tạo report có `crash_safety = 20/20`. Suite này chủ yếu kiểm host và swarm; test riêng kiểm workflow trực tiếp. Chưa có benchmark chính thức.

## 5. Công cụ AI đã dùng

- Codex: giải thích yêu cầu lab và swarm tham chiếu, hỗ trợ triển khai workflow CP2, hướng dẫn CP3, viết test CP4, chạy kiểm tra và hỗ trợ viết báo cáo.
- Bằng chứng kiểm chứng trong phiên làm việc: đối chiếu code với docstring và contract, chạy test student của workflow và bộ test mặc định. Phần tự kiểm tra do cá nhân thực hiện cần được xác nhận trước khi nộp.

## 6. Tự đánh giá

Tự đánh giá cá nhân: hoàn thành phần việc đã giao, bài làm không yêu cầu phải hoạt động teamwork quá nhiều.
