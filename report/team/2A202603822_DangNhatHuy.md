# Báo cáo cá nhân — 2A202603822 Đặng Nhật Huy

## 1. Thông tin thành viên

- Họ tên: Đặng Nhật Huy
- MSSV: 2A202603822
- Email: 26ai.huydn@vinuni.edu.vn
- GitHub: huydn8816

## 2. Phần việc phụ trách

Shape B `single` (một agent ReAct) trong `src/lab8/shapes/single.py`, và file test riêng `src/tests/test_single_shape.py` cho shape này.

## 3. Đóng góp cụ thể

- **Commit chính:** `0970390` (nhánh `feat/shape-b-single`): `feat(shape-b): implement single ReAct shape and host-side tests`.
- **Code:** `src/lab8/shapes/single.py`
  - `run_claim` mở connection, bọc lỗi để không ném exception, đóng connection ở `finally`. `InjectedCrash` được ném lên caller sau khi ghi trace.
  - `decide` chỉ chọn tool đọc: `lookup_order` rồi `compute_compensation` trên dòng order. Không đọc nội dung ticket.
  - Số tiền lấy từ `compute_compensation`. Quote bằng 0 thì `denied`. Quote lớn hơn 0 thì truyền **quote đầy đủ** vào `durability.issue_refund` với `crash_at`.
  - Trace chỉ ghi các field đã qua allowlist.
- **Test:** `src/tests/test_single_shape.py`, 5 nhóm test (20 test case khi parametrize):
  1. Ticket ghi sai số ngày không làm đổi số tiền (C-001).
  2. Trace không chứa nội dung ticket hay secret, chạy với 5 seed (C-001, C-005, C-009).
  3. Số model call và tool call cố định trên đường đầy đủ (C-001: 3 và 3).
  4. Thiếu `order_id` dừng sớm, không ghi ledger (C-004).
  5. Crash rồi resume vẫn chỉ một refund (C-001, hai điểm crash).
- **Quyết định kỹ thuật:**
  - Không để `decide` đọc ticket, vì ticket là dữ liệu người dùng.
  - Không tự trừ phần đã hoàn trước đó. Host làm việc này, nên shape truyền quote đầy đủ.
  - Mỗi bước `decide` gọi `complete()` một lần để chi phí model được tính vào Budget, giúp so sánh với các shape khác.
  - Không dùng `lookup_refund_history` vì host đã tự kiểm trần theo đơn.

## 4. Bằng chứng

Chạy trong thư mục `src/`, Python 3.14, venv `.venv`:

- `python -m pytest -q -m student -o addopts= -k "single and not workflow and not orchestrator and not swarm"` → **62 passed**. Gồm T01–T10, T13, T14, T11, T12 cho shape `single`.
- `python -m pytest -q tests/test_single_shape.py` → **20 passed**.
- `python -m pytest -q` (cổng host mặc định) → **74 passed**, 248 deselected.
- `python -m lab8.crash_test --count 20` chạy thử ra `crash_safety 20/20`. Đây là lần chạy thử, không phải file chính thức. Số chính thức nằm trong `src/reports/crash.json` do lệnh lab tạo.

Chưa chạy benchmark chính thức (`lab8.benchmark`), nên chưa có số pass rate hay cost của shape B trong `benchmark.json`.

## 5. Công cụ AI đã dùng

- **Claude Code** (trợ lý AI trong terminal): đọc đề bài và tài liệu, đề xuất cách chia việc, viết `single.py`, viết `test_single_shape.py`, chạy test.
- **Cách tự kiểm tra:** đọc lại code `single.py` so với docstring và `docs/business_rules.md`, `docs/contracts.md`. Chạy lại test student và test riêng, xem output thật thay vì tin vào lời của trợ lý.
- **Lưu ý:** hàm `decide` của shape B là quy tắc cố định, không phải model thật. Đây là lựa chọn để kết quả ổn định trên MockLLM. Nếu giảng viên yêu cầu model tự chọn tool, phần này cần viết lại.

## 6. Tự đánh giá

- **Làm tốt:** shape B qua 62 test student và 20 test riêng. Số tiền không phụ thuộc ticket. Trace không lộ nội dung cần giấu.
- **Còn thiếu:** chưa điền dòng vào bảng đóng góp `TEAM.md`, chưa chạy benchmark chính thức, chưa điền số vào `decision_adr.md`.
- **Việc tiếp theo:** commit có nội dung kỹ thuật, điền `TEAM.md`, và đưa phần của mình cho người tổng hợp theo file `report/team/2A202603822_DangNhatHuy_group_part.md`.
