# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên           | MSSV        | Email                        | GitHub          | Vai trò                                             |
| --: | ---------------- | ----------- | ---------------------------- | --------------- | --------------------------------------------------- |
|   1 | Nguyễn Thành Nam | 2A202603934 | ishodajo@gmail.com           | Ishodayo        | Orchestrator + handoff (shape C)                    |
|   2 | Nguyễn Tiến Đạt  | 2A202603752 | nguyentiendatqb126@gmail.com | chesschillchill | Workflow (shape A) + kiểm tra an toàn               |
|   3 | Đặng Nhật Huy    | 2A202603822 | 26ai.huydn@vinuni.edu.vn     | huydn8816       | Single agent (shape B) + test                       |
|   4 | Trần Quang Hưng  | 2A202603767 |                              | tqhungdl        | Tổng hợp báo cáo, phân tích benchmark, decision ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người                          | Vai                                            | Commit                                                                                   | Test đã thêm hoặc sửa                               |
| ------------------------------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Nguyễn Thành Nam (2A202603934) | Orchestrator + handoff (shape C)               | `5be3a3a` orchestrator.py; `66a5efa` test_orchestrator_boundary.py                       | `src/tests/test_orchestrator_boundary.py` (24 test) |
| Nguyễn Tiến Đạt (2A202603752)  | Workflow (shape A), CP2–CP4 + kiểm tra an toàn | `4ca802c` workflow.py (CP2–CP3); `b389b75` test_workflow_safety.py và crash report (CP4) | `src/tests/test_workflow_safety.py` (11 test)       |

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
- Báo cáo cá nhân: `report/team/2A202603934_NguyenThanhNam.md`; phần nhóm: mục _Shape C - Orchestrator_ trong `report/team/group_report.md`.

## 2A202603752_NguyenTienDat

### Phần việc phụ trách

- Shape A — workflow trong `src/lab8/shapes/workflow.py`, phạm vi CP2–CP4; bổ sung kiểm tra approval, trace/stdout và phục hồi sau crash.

### Đóng góp cụ thể

- `4ca802c`: triển khai workflow CP2–CP3. Đọc claim bằng `get_claim_view`, kiểm tra order và quyền sở hữu qua `lookup_order`, tính quote bằng `compute_compensation` từ dữ liệu database; không dùng nội dung ticket để quyết định số tiền. Quote dương được truyền đầy đủ vào `issue_refund`; host kiểm approval, giới hạn số tiền và trừ phần đã hoàn. Workflow không tự ghi ledger và không gọi MockLLM.
- Truyền `crash_at` vào `issue_refund`, để `InjectedCrash` truyền ra ngoài và đóng kết nối bằng `finally`. Dùng `finish()` để trả `RunResult` và ghi trace ở các nhánh kết thúc bình thường; trace chỉ ghi order view đã lọc, quote và quyết định, không ghi ticket hoặc nguyên claim row.
- `b389b75`: thêm `src/tests/test_workflow_safety.py` (11 test) kiểm tra approval, trace/stdout và phục hồi ở ba vị trí crash; chạy crash suite tạo `src/reports/crash.json`.

### Bằng chứng

- Theo kết quả CP4 trong báo cáo cá nhân, chạy trong `src/`: `python -m pytest -q tests/test_workflow_safety.py` → 11 passed; `python -m pytest -q -m student -o addopts= -k workflow` → 62 passed; `python -m pytest -q` → 85 passed.
- T11 (`test_t11_retry_keeps_one_refund`) và T12 (`test_t12_crash_before_checkpoint_does_not_double_pay`) đã pass: chạy lại và crash rồi resume vẫn giữ một refund và một audit `refund_committed`.
- `python -m lab8.crash_test --count 20 --out reports/crash.json` → `crash_safety = 20/20`. Suite này chủ yếu kiểm host và swarm; workflow được kiểm trực tiếp qua 11 test riêng.

## 2A202603767_Trần Quang Hưng

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
