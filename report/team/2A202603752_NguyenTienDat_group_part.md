# Hướng dẫn điền báo cáo nhóm — Nguyễn Tiến Đạt — Workflow

Chỉ bổ sung phần workflow CP2–CP4. Giữ nguyên `group_report.md` cho người tổng hợp.

## Mục 3 — Giải pháp

Có thể chèn đoạn sau vào phần mô tả shape A:

Shape A (`src/lab8/shapes/workflow.py`) thực hiện chuỗi bước Python cố định: đọc claim, kiểm tra order và quyền sở hữu, tính compensation rồi gọi host. Số tiền lấy từ `compute_compensation` trên dữ liệu order trong database, không lấy từ lời khai trong ticket. Quote bằng 0 thì từ chối; quote dương được truyền đầy đủ vào `issue_refund`. Host kiểm approval, áp trần và trừ các refund trước của cùng order. Workflow không gọi MockLLM và không tự ghi ledger.

Workflow truyền `crash_at` cho host và để `InjectedCrash` truyền ra ngoài; kết nối được đóng trong `finally`. Các nhánh kết thúc bình thường dùng `finish()` để ghi trace và tạo `RunResult`. Trace ghi order view đã lọc, quote và quyết định; không ghi ticket hoặc nguyên claim row. Workflow không có handoff.

## Mục 4 — Kết quả

Điền crash safety **20/20**, nguồn `src/reports/crash.json` do công cụ lab sinh ra. Suite này chủ yếu kiểm host và swarm; workflow được kiểm trực tiếp qua 11 test trong `test_workflow_safety.py` về approval, trace/stdout và ba vị trí crash. Chưa điền bảng so sánh kiến trúc vì chưa có benchmark chính thức.

## Mục 5 — Khó khăn và cách xử lý

Có thể chèn:

Khi mới hoàn thành CP2, test workflow có 61 passed và 1 failed tại T12 với thông báo `crash did not fire`. Nguyên nhân là workflow chưa truyền `crash_at` xuống `issue_refund`, nên tình huống crash không được kích hoạt. Sau khi bổ sung tham số này ở CP3 và để `InjectedCrash` truyền ra ngoài, chạy lại `python -m pytest -q -m student -o addopts= -k workflow` đạt 62 passed.

## Mục 6 — Tổng hợp đóng góp

Có thể ghi: Nguyễn Tiến Đạt (2A202603752) phụ trách workflow CP2–CP4; commit CP2–CP3 `4ca802c`, commit CP4 `b389b75`; bổ sung `src/tests/test_workflow_safety.py` (11 test). Cần cập nhật bảng đóng góp `TEAM.md` với các hash này.

## Mục 7 — Hạn chế và hướng cải thiện

Có thể bổ sung: workflow đã qua test public và kiểm tra an toàn CP4; chưa có benchmark chính thức để chọn kiến trúc cuối cùng hoặc kết luận về hidden pass rate. Crash suite 20/20 không chứng minh tất cả shape đã hoàn thành.
