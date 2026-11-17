# Team

## Thông tin nhóm

- Tên nhóm: 777
- Lớp: L3B
- Repo nhóm: `K5-L3B-Day08-777-FromWorkflowstoAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/tqhungdl/K5-L3B-Day08-777-FromWorkflowstoAgents, nhánh `main`, commit chốt:

## Thành viên

| STT | Họ tên           | MSSV        | Email                        | GitHub          | Vai trò                                             |
| --: | ---------------- | ----------- | ---------------------------- | --------------- | --------------------------------------------------- |
|   1 | Nguyễn Thành Nam | 2A202603934 | ishodajo@gmail.com           | Ishodayo        | Orchestrator + handoff (shape C)                    |
|   2 | Nguyễn Tiến Đạt  | 2A202603752 | nguyentiendatqb126@gmail.com | chesschillchill | Workflow (shape A) + kiểm tra an toàn               |
|   3 | Đặng Nhật Huy    | 2A202603822 | 26ai.huydn@vinuni.edu.vn     | huydn8816       | Single agent (shape B) + test                       |
|   4 | Trần Quang Hưng  | 2A202603767 | tqhungdl0206@gmail.com       | tqhungdl        | Tổng hợp báo cáo, phân tích benchmark, decision ADR |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người                          | Vai                                            | Commit                                                                                   | Test đã thêm hoặc sửa                               |
| ------------------------------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Nguyễn Thành Nam (2A202603934) | Orchestrator + handoff (shape C)               | `5be3a3a` orchestrator.py; `66a5efa` test_orchestrator_boundary.py                       | `src/tests/test_orchestrator_boundary.py` (24 test) |
| Nguyễn Tiến Đạt (2A202603752)  | Workflow (shape A), CP2–CP4 + kiểm tra an toàn | `4ca802c` workflow.py (CP2–CP3); `b389b75` test_workflow_safety.py và crash report (CP4) | `src/tests/test_workflow_safety.py` (11 test)       |
| Đặng Nhật Huy | Shape B `single` (`src/lab8/shapes/single.py`) | `0970390` (nhánh `feat/shape-b-single`) | `src/tests/test_single_shape.py` (5 nhóm test) |
| Trần Quang Hưng (2A202603767) | Tổng hợp báo cáo nhóm, phân tích benchmark và decision ADR | `965475c` tổng hợp báo cáo, kết quả benchmark và decision ADR |  |

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
- Rà soát bài nộp của nhóm theo rubric và template; kiểm tra lại phần ablation R2 (`src/reports/ablation_r2.json`).

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

## 2A202603822_DangNhatHuy

### Phần việc phụ trách

- Shape B `single` (một agent ReAct) trong `src/lab8/shapes/single.py`, và test riêng `src/tests/test_single_shape.py`.

### Đóng góp cụ thể

- Commit `0970390` (nhánh `feat/shape-b-single`): code shape B và test riêng.
- Test: 5 nhóm test trong `src/tests/test_single_shape.py` (ticket không đổi số tiền; trace không chứa ticket hay secret, 5 seed; số model/tool call cố định; thiếu `order_id` dừng sớm; crash rồi resume giữ một refund).
- Quyết định kỹ thuật: `decide` không đọc ticket; shape truyền quote đầy đủ vào `issue_refund` và để host trừ phần đã hoàn; trace chỉ ghi các field đã qua allowlist.

### Bằng chứng

- `pytest -q -m student -o addopts= -k "single and not workflow and not orchestrator and not swarm"` → 62 passed.
- `pytest -q tests/test_single_shape.py` → 20 passed.
- Báo cáo cá nhân: `report/team/2A202603822_DangNhatHuy.md`.

## 2A202603767_TranQuangHung

### Phần việc phụ trách

- Tổng hợp báo cáo nhóm, phân tích benchmark bốn shape và lập decision ADR; hoàn thiện research card R2, thực hiện ablation và tổng hợp bằng chứng kiểm thử.

### Đóng góp cụ thể

- Tổng hợp phần giải pháp của các thành viên vào `report/team/group_report.md`; lập bảng kết quả từ `src/reports/benchmark.json`, so sánh pass rate, pass^5, seed variance, cost/success và mean/p95 steps.
- Lập luận chọn workflow trong `report/team/decision_adr.md` dựa trên kết quả public: 70/70 trial pass, chi phí mô phỏng 27.86 VND/success và 2.79 bước trung bình; phân biệt kết quả public với khả năng đáp ứng bộ hidden.
- Hoàn thiện `report/team/research_card.md` theo R2 và paper MAST (NeurIPS 2025), phân biệt kết luận của nguồn, cách phân loại lỗi của nhóm, hypothesis và kết quả thực nghiệm.
- Chạy benchmark đối chứng bằng cùng evaluator trên 14 claim và 5 seed, tạo `src/reports/ablation_r2.json`; ghi kết quả trước–sau và giới hạn nghiên cứu vào research card. Commit `965475c` chứa báo cáo, benchmark và phần thực nghiệm liên quan.

### Bằng chứng

- `src/reports/benchmark.json`: workflow, single và orchestrator đạt 70/70 trial pass; swarm đạt 69/70.
- Tài liệu tổng hợp: `report/team/group_report.md`, `report/team/decision_adr.md`, `report/team/research_card.md`; phần thực nghiệm và kiểm thử được hỗ trợ bởi Codex, kết quả đối chiếu với file JSON do công cụ sinh ra.
