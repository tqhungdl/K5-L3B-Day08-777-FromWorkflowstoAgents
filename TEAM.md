# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Thành Nam | 2A202603934 | ishodajo@gmail.com | Ishodayo | Orchestrator + handoff (shape C) |
|   2 | Nguyễn Tiến Đạt | 2A202603752 |       | chesschillchill | Workflow (shape A) + kiểm tra an toàn |
|   3 | Đặng Nhật Huy | 2A202603822 | 26ai.huydn@vinuni.edu.vn | huydn8816 | Single agent (shape B) + test |
|   4 | Trần Quang Hưng | 2A202603767 |       | tqhungdl | Tổng hợp báo cáo, phân tích benchmark, decision ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Thành Nam (2A202603934) | Orchestrator + handoff (shape C) | `5be3a3a` orchestrator.py; `66a5efa` test_orchestrator_boundary.py | `src/tests/test_orchestrator_boundary.py` (24 test) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-

## 2A202603934_NguyenThanhNam

### Phần việc phụ trách

- Shape C `orchestrator` (orchestrator + investigator chỉ đọc) trong `src/lab8/shapes/orchestrator.py`, handoff giữa hai tầng và trace an toàn của shape C.

### Đóng góp cụ thể

- `5be3a3a`: viết `orchestrator.py`. Orchestrator đọc claim qua `get_claim_view`, dựng handoff bằng `make_handoff` (`facts` rỗng, chỉ tool đọc), investigator chạy qua `run_readonly_investigators`, tiền do `compute_compensation` tính, chỉ orchestrator gọi `durability.issue_refund` với quote đầy đủ và `crash_at`.
- `66a5efa`: thêm `src/tests/test_orchestrator_boundary.py` (24 test): cổng approval (thiếu, thu hồi, hết hạn, mượn của claim khác), sai principal, ticket injection, handoff chỉ có tool đọc, trace không lộ secret/PII trên 14 claim public, crash ở 3 điểm rồi chạy lại vẫn một refund.

### Bằng chứng

- `python -m pytest -q -m student -o addopts= -k orchestrator` → 62 passed.
- `python -m pytest -q tests/test_orchestrator_boundary.py` → 24 passed.
- Báo cáo cá nhân: `report/team/2A202603934_NguyenThanhNam.md`; phần nhóm: mục *Shape C - Orchestrator* trong `report/team/group_report.md`.

## 2A202603767_Trần Quang Hưng

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
