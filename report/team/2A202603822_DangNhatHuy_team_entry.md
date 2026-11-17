# Dòng của Đặng Nhật Huy (2A202603822) để điền vào TEAM.md

File này chỉ để người tổng hợp copy vào `TEAM.md`. Không sửa `TEAM.md` trực tiếp từ file này.

Written for: người tổng hợp `TEAM.md` (copy đúng dòng, giữ nguyên định dạng bảng).

## Bảng thành viên (`## Thành viên`)

Điền vào một dòng trống của bảng, nên chọn dòng trống còn lại để tránh trùng với người khác:

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| | Đặng Nhật Huy | 2A202603822 | 26ai.huydn@vinuni.edu.vn | huydn8816 | Shape B `single` |

## Bảng đóng góp (`## Bảng đóng góp`)

Điền vào một dòng trống của bảng:

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Đặng Nhật Huy | Shape B `single` (`src/lab8/shapes/single.py`) | `0970390` (nhánh `feat/shape-b-single`) | `src/tests/test_single_shape.py` (5 nhóm test) |

Lưu ý: `python -m lab8.check_submission` đọc bảng này bằng máy. Giữ nguyên tiêu đề và thứ tự cột. Nếu check báo lỗi ở cột Commit, bỏ phần tên nhánh và chỉ giữ hash.

## Mục cá nhân (`## MSSV_HoTen`)

Copy khối này xuống cuối `TEAM.md`, thay `MSSV_HoTen` bằng `2A202603822_DangNhatHuy`:

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
