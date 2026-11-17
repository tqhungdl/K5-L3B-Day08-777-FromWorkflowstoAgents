# Phần báo cáo nhóm — Nguyễn Thành Nam (2A202603934) — Shape C (orchestrator + handoff)

---

## Copy vào mục 3 "Giải pháp" của group_report.md

Shape C (`src/lab8/shapes/orchestrator.py`) có hai tầng. **Orchestrator** đọc claim qua `get_claim_view` và là bên duy nhất được gọi `durability.issue_refund`. **Investigator** (`lab8.runtime.run_readonly_investigators`) chỉ nhận handoff và chạy các tool đọc ghi trong đó với `worker=True`, nên mọi lời gọi tool ghi đều bị chặn.

Luồng: thiếu claim → `failed`; thiếu `order_id` → `needs_info`; dựng handoff; investigator đọc `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`; đơn không thấy được → `escalated`; quote = 0 → `denied` (không gọi host); quote > 0 → orchestrator gọi `issue_refund` với **quote đầy đủ** và `crash_at`, host quyết `resolved` / `denied` (có `policy_denied`) / `failed` (conflict).

Ranh giới code / model: số tiền do `compute_compensation` tính trên order row; ticket không được đọc để lấy mã đơn hay số ngày trễ; MockLLM chỉ soạn lời đáp một lần với prompt chỉ chứa status.

**Handoff được sanitize bằng allowlist trong code**, không bằng tóm tắt LLM: `make_handoff` chỉ giữ 8 field (`contract_version`, `request_id`, `claim_id`, `principal_scope`, `task`, `facts`, `allowed_tools`, `max_output_tokens`), từ chối tool ghi và từ chối payload còn `CANARY_SECRET_` / `parent_secret` / `raw_headers`. Shape C để `facts={}`: không có dữ kiện nào từ parent context đi qua ranh giới; investigator tự đọc order qua tool có kiểm principal.

**Trace** của shape C có 6 loại event: `claim` (chỉ `claim_id`, `has_order_id`), `handoff` (bản đã sanitize), `investigator` (order view 7 field đã lọc, số đã hoàn, số policy), `quote`, `host` (`ok`, `reason`, `conflict`), `decision`. Cố ý **không ghi**: nội dung ticket, `parent_secret`, raw header, claim row, order row thô (SĐT, địa chỉ, tên hàng, internal note), output của MockLLM. Khi crash, trace được ghi trước khi `InjectedCrash` được ném lại.

---

## Copy vào mục 4 "Kết quả" của group_report.md

Kết quả kiểm tra của shape C trong quá trình phát triển (tham khảo, không thay thế số trong file report):
- Test student `-k orchestrator`: 62 passed.
- Test riêng `src/tests/test_orchestrator_boundary.py`: 24 passed.

---

## Copy vào mục 5 "Khó khăn và cách xử lý" của group_report.md

- **Phiên bản Python:** máy chỉ có Python 3.15, ngoài khoảng 3.11–3.13 của đề. Dùng `uv venv --python 3.12 .venv` để tải Python 3.12 và tạo venv; smoke và pytest chạy được.
- **Kiểm crash cho shape của mình:** `lab8.crash_test` chỉ kiểm host và swarm, không chạy orchestrator. Xử lý: dựa vào T12 trong ma trận student và thêm 3 test crash-rồi-chạy-lại cho orchestrator trong `test_orchestrator_boundary.py`.
- **Bộ public thiếu một số nhánh approval** (thu hồi, mượn approval của claim khác, sai principal) mà bộ hidden có kiểm. Xử lý: thêm claim giả vào store trong test để phủ các nhánh này.

---

## Copy vào mục 6 "Tổng hợp đóng góp" (tham khảo, bảng chính nằm trong TEAM.md)

- Nguyễn Thành Nam (2A202603934): shape C `src/lab8/shapes/orchestrator.py` (commit `5be3a3a`); test `src/tests/test_orchestrator_boundary.py` (commit `66a5efa`).
