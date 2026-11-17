# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: 777
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`):

## 2. Mục tiêu và cách tiếp cận

Mục tiêu của nhóm là so sánh bốn kiến trúc workflow, single agent, orchestrator và swarm, từ đó lựa chọn kiến trúc có mức tự chủ thấp nhất nhưng vẫn đáp ứng yêu cầu về tính đúng đắn, an toàn và chi phí.

Trong quá trình xử lý, code chịu trách nhiệm tính số tiền hoàn, kiểm tra chính sách và approval, đồng thời bảo đảm một claim không được hoàn tiền nhiều lần khi chạy lại hoặc sau sự cố. Model chỉ hỗ trợ đọc thông tin, lựa chọn công cụ đọc và soạn nội dung. Dữ liệu trong ticket được xem là dữ liệu đầu vào, không phải chỉ dẫn để thay đổi quy trình hoặc bỏ qua chính sách.

Nhóm phân công Đạt phụ trách workflow, Huy phụ trách single agent, Nam phụ trách orchestrator và Hưng phụ trách tổng hợp bằng chứng, phân tích kết quả và viết báo cáo. 

Để so sánh công bằng, nhóm đánh giá các kiến trúc trên cùng tập claim, cùng các seed 11,22,33,44,55, cùng MockLLM, công cụ và bảng giá. Việc lựa chọn kiến trúc dựa trên pass rate, pass⁵, độ biến động giữa các seed, chi phí mô phỏng trên mỗi lần thành công và số bước xử lý; đồng thời kiểm tra khả năng phục hồi sau crash, bảo vệ secret và tuân thủ approval.

## 3. Giải pháp

#### Shape A - Workflow
Shape A (`src/lab8/shapes/workflow.py`) thực hiện chuỗi bước Python cố định: đọc claim, kiểm tra order và quyền sở hữu, tính compensation rồi gọi host. Số tiền lấy từ `compute_compensation` trên dữ liệu order trong database, không lấy từ lời khai trong ticket. Quote bằng 0 thì từ chối; quote dương được truyền đầy đủ vào `issue_refund`. Host kiểm approval, áp trần và trừ các refund trước của cùng order. Workflow không gọi MockLLM và không tự ghi ledger.

Workflow truyền `crash_at` cho host và để `InjectedCrash` truyền ra ngoài; kết nối được đóng trong `finally`. Các nhánh kết thúc bình thường dùng `finish()` để ghi trace và tạo `RunResult`. Trace ghi order view đã lọc, quote và quyết định; không ghi ticket hoặc nguyên claim row. Workflow không có handoff.

#### Shape B - Single

Shape B (`src/lab8/shapes/single.py`) là một vòng ReAct, giới hạn 8 bước qua `lab8.runtime.run_react`. Hàm `decide` chỉ chọn tool đọc: `lookup_order` rồi `compute_compensation` trên dòng order lấy từ DB. Hàm này không đọc nội dung ticket, nên số ngày trễ người dùng ghi trong ticket không ảnh hưởng đến số tiền. Mỗi bước gọi `complete()` để ghi vào Budget, giúp chi phí so sánh được với các shape khác.

Ranh giới code và model: `decide` chỉ chọn tool đọc. Số tiền do `compute_compensation` tính. Shape truyền **quote đầy đủ** vào `durability.issue_refund`; host tự trừ phần đã hoàn trước đó và kiểm approval. Shape không tự ghi ledger.

Trace ghi các event đã qua allowlist: kết quả `lookup_order` đã lọc, quote, quyết định, kết quả host. Shape không ghi nội dung ticket và không ghi nguyên claim row hay order row. Khi crash được chỉ định (`crash_at`), trace được ghi trước khi `InjectedCrash` được ném lên caller.

#### Shape C - Orchestrator

Shape C (`src/lab8/shapes/orchestrator.py`) có hai tầng. **Orchestrator** đọc claim qua `get_claim_view` và là bên duy nhất được gọi `durability.issue_refund`. **Investigator** (`lab8.runtime.run_readonly_investigators`) chỉ nhận handoff và chạy các tool đọc ghi trong đó với `worker=True`, nên mọi lời gọi tool ghi đều bị chặn.

Luồng: thiếu claim → `failed`; thiếu `order_id` → `needs_info`; dựng handoff; investigator đọc `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`; đơn không thấy được → `escalated`; quote = 0 → `denied` (không gọi host); quote > 0 → orchestrator gọi `issue_refund` với **quote đầy đủ** và `crash_at`, host quyết `resolved` / `denied` (có `policy_denied`) / `failed` (conflict).

Ranh giới code / model: số tiền do `compute_compensation` tính trên order row; ticket không được đọc để lấy mã đơn hay số ngày trễ; MockLLM chỉ soạn lời đáp một lần với prompt chỉ chứa status.

**Handoff được sanitize bằng allowlist trong code**, không bằng tóm tắt LLM: `make_handoff` chỉ giữ 8 field (`contract_version`, `request_id`, `claim_id`, `principal_scope`, `task`, `facts`, `allowed_tools`, `max_output_tokens`), từ chối tool ghi và từ chối payload còn `CANARY_SECRET_` / `parent_secret` / `raw_headers`. Shape C để `facts={}`: không có dữ kiện nào từ parent context đi qua ranh giới; investigator tự đọc order qua tool có kiểm principal.

**Trace** của shape C có 6 loại event: `claim` (chỉ `claim_id`, `has_order_id`), `handoff` (bản đã sanitize), `investigator` (order view 7 field đã lọc, số đã hoàn, số policy), `quote`, `host` (`ok`, `reason`, `conflict`), `decision`. Cố ý **không ghi**: nội dung ticket, `parent_secret`, raw header, claim row, order row thô (SĐT, địa chỉ, tên hàng, internal note), output của MockLLM. Khi crash, trace được ghi trước khi `InjectedCrash` được ném lại.

## 4. Kết quả

Kết quả lấy từ `src/reports/benchmark.json`: mỗi shape chạy trên cùng 14 claim public với 5 seed `11,22,33,44,55`, tương ứng 70 trial/shape và 280 trial tổng cộng. Các lần chạy dùng cùng MockLLM, bảng giá và ngày chính sách `2026-11-15`; mỗi trial dùng một SQLite mới.

| Shape | Trial pass | Pass rate | Pass⁵ | Seed min–max | Seed variance | Cost/success (VND mô phỏng) | Mean/p95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Workflow | 70/70 | 100.00% | 100.00% | 100.00–100.00% | 0 | 27.86 | 2.79 / 3 |
| Single | 70/70 | 100.00% | 100.00% | 100.00–100.00% | 0 | 28.94 | 3.79 / 4 |
| Orchestrator | 70/70 | 100.00% | 100.00% | 100.00–100.00% | 0 | 56.66 | 5.36 / 6 |
| Swarm | 69/70 | 98.57% | 92.86% | 92.86–100.00% | 0.00081633 | 49.57 | 2.80 / 3 |

Latency của MockLLM là `unavailable`.

crash_safety: 20/20

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Lỗi gặp phải (kèm lệnh, output hoặc ảnh chụp) và cách nhóm xử lý.

...
#### Shape A - Workflow

Khi mới hoàn thành CP2, test workflow có 61 passed và 1 failed tại T12 với thông báo `crash did not fire`. Nguyên nhân là workflow chưa truyền `crash_at` xuống `issue_refund`, nên tình huống crash không được kích hoạt. Sau khi bổ sung tham số này ở CP3 và để `InjectedCrash` truyền ra ngoài, chạy lại `python -m pytest -q -m student -o addopts= -k workflow` đạt 62 passed.

#### Shape B - Single

- **Môi trường Python:** máy chỉ có Python 3.14, README ghi 3.11–3.13. Tạo venv bằng `py -3 -m venv .venv` rồi cài `requirements.txt` vẫn chạy được pytest và smoke test. Cần kiểm tra lại trên máy khác nếu có lỗi.
- **Chạy test có filter `-k`:** `-k single` khớp cả tên hàm test dùng chung nên chạy cả shape workflow và orchestrator (đang là stub). Cách xử lý: lọc bằng `-k "single and not workflow and not orchestrator and not swarm"`.

#### Shape C - Orchestrator

- **Phiên bản Python:** máy chỉ có Python 3.15, ngoài khoảng 3.11–3.13 của đề. Dùng `uv venv --python 3.12 .venv` để tải Python 3.12 và tạo venv; smoke và pytest chạy được.
- **Kiểm crash cho shape của mình:** `lab8.crash_test` chỉ kiểm host và swarm, không chạy orchestrator. Xử lý: dựa vào T12 trong ma trận student và thêm 3 test crash-rồi-chạy-lại cho orchestrator trong `test_orchestrator_boundary.py`.
- **Bộ public thiếu một số nhánh approval** (thu hồi, mượn approval của claim khác, sai principal) mà bộ hidden có kiểm. Xử lý: thêm claim giả vào store trong test để phủ các nhánh này.


## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

- Trần Quang Hưng (2A202603767): viết báo cáo `report/team/group_report.md`, chạy test chung, tổng hợp dữ liệu, tổng hợp thông tin trong `report/team/decision_adr.md`. 

- Nguyễn Tiến Đạt (2A202603752): phụ trách shape A workflow CP2–CP4; commit CP2–CP3 `4ca802c`, commit CP4 `b389b75`; bổ sung `src/tests/test_workflow_safety.py` (11 test).

- Đặng Nhật Huy (2A202603822): shape B single `src/lab8/shapes/single.py`; test `src/tests/test_single_shape.py` (5 nhóm test). Commit hash: 0970390.

- Nguyễn Thành Nam (2A202603934): shape C orchestrator `src/lab8/shapes/orchestrator.py` (commit `5be3a3a`); test `src/tests/test_orchestrator_boundary.py` (commit `66a5efa`).

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`.

Workflow đã qua test public và kiểm tra an toàn CP4; chưa có benchmark chính thức để chọn kiến trúc cuối cùng hoặc kết luận về hidden pass rate. Crash suite 20/20 không chứng minh tất cả shape đã hoàn thành.

## 8. Tài liệu tham khảo

...
