# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: a5c93e4
- Run id dẫn chứng: R-workflow-C-001-s11 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000 - 1.000 / 0.000
- Cost per success (mô phỏng, VND): 27.86 VND
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 4 passed / 11 passed

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Nhóm chọn workflow vì trên cùng 14 claim public và 5 seed, workflow đạt pass rate 100%, pass⁵ 100% và seed variance bằng 0, tương đương single agent và orchestrator. Đồng thời, workflow có chi phí mô phỏng trên mỗi trial thành công thấp nhất (27.86 VND) và số bước trung bình thấp nhất (2.79). Với bài toán xử lý claim theo các quy tắc xác định, kết quả hiện tại chưa cho thấy lợi ích của việc tăng mức tự chủ. Vì vậy, workflow phù hợp với mục tiêu chọn kiến trúc ít tự chủ nhất nhưng vẫn đáp ứng yêu cầu.

## Có đáng đổi lấy multi-agent không

Trên bộ test hiện tại, nhóm chưa thấy lợi ích đủ lớn để chuyển từ workflow sang multi-agent. Workflow và orchestrator cùng đạt pass rate 100%, pass⁵ 100% và seed variance bằng 0, nhưng orchestrator có cost/success cao hơn (56.66 VND so với 27.86 VND mô phỏng) và trung bình có nhiều bước hơn (5.36 so với 2.79). Vì vậy, nhóm giữ workflow. Nhóm sẽ xem xét lại nếu đánh giá trên dữ liệu rộng hơn cho thấy multi-agent cải thiện đáng kể độ chính xác hoặc xử lý được các tác vụ cần điều tra song song mà workflow không đáp ứng, với chi phí chấp nhận được và vẫn bảo đảm approval, bảo mật và chống hoàn tiền trùng.

## Trace và bằng chứng

Trace của nhóm ghi những event nào? Field nào cố ý **không** ghi, và vì sao? Nếu trace nằm ngoài chỗ scanner quét được, đội security chứng minh thế nào là hệ thống không lộ secret?

Trace của workflow ghi thông tin order đã lọc, quote và quyết định xử lý; các nhánh kết thúc bình thường dùng `finish()` để ghi trace và tạo `RunResult`. Nhóm cố ý không ghi nội dung ticket, nguyên claim row hoặc order row, `parent_secret`, raw headers, số điện thoại, địa chỉ, tên hàng và ghi chú nội bộ nhằm hạn chế lộ secret và dữ liệu cá nhân.

Bằng chứng đánh giá nằm trong `src/reports/benchmark.json`, gồm 70/70 trial workflow pass; một run id tham chiếu là `R-workflow-C-001-s11`. Test `test_trace_and_stdout_exclude_sensitive_data` trong `src/tests/test_workflow_safety.py` kiểm tra file trace, kết quả trả về để phát hiện secret hoặc chuỗi bị cấm. 

Nếu trace nằm ngoài đường dẫn scanner mặc định, cần đưa đường dẫn thực tế vào phạm vi kiểm tra và xác nhận file tồn tại, đọc được, thuộc đúng lần chạy trước khi kết luận không phát hiện rò rỉ.

## Giới hạn

MockLLM không phải model sản xuất. Latency để `unavailable`. Không sửa JSON cho đủ 0.75.
