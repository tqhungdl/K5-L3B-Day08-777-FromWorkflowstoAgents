# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 |
SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Mert Cemri và cộng sự (2025), [Why Do Multi-Agent LLM Systems Fail?](https://proceedings.neurips.cc/paper_files/paper/2025/file/b1041e52d3be19f0a9bc491657488e4a-Paper-Datasets_and_Benchmarks_Track.pdf), NeurIPS 2025, Datasets and Benchmarks Track. Bằng chứng: dataset trace có gán nhãn và phân tích thực nghiệm. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST phân biệt 14 kiểu lỗi trong ba nhóm: thiết kế hệ thống, lệch phối hợp giữa agent và kiểm chứng tác vụ. FM-3.3 (Incorrect Verification) bao gồm việc đối chiếu thông tin quan trọng không đầy đủ hoặc sai; thêm verifier không tự bảo đảm hệ thống thành công (mục 4, phụ lục A). |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nghiên cứu phân tích 1,642 trace từ 7 hệ thống MAS, trên tác vụ lập trình, toán và agent tổng quát, với các họ model GPT-4, Claude, Qwen2.5 và CodeLlama. Phạm vi này khác LogiX-VN dùng MockLLM; taxonomy không được khẳng định bao phủ mọi lỗi. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Nếu tắt riêng cơ chế swarm ghi đè delay_days của database bằng số ngày trong ticket, dự đoán C-002 ở seed 55 sẽ pass: pass rate tăng từ 69/70 (98.57%) lên 70/70 (100%), pass^5 từ 13/14 (92.86%) lên 14/14 (100%), seed variance từ 0.00081633 về 0. Đây là dự đoán sau khi quan sát baseline, cần kiểm tra bằng variant. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | So baseline swarm với một variant riêng luôn giữ delay_days từ database. Chỉ tắt nhánh REFERENCE_WEAKNESS ghi đè delay_days; giữ nguyên topology, prompt, lời gọi model, tools, 14 claim public, seed 11,22,33,44,55, as_of 2026-11-15, bảng giá và evaluator. Mỗi trial dùng SQLite mới. Đặt variant và runner ở file thử nghiệm riêng, không sửa swarm tham chiếu hay file thước đo. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Nhóm diễn giải lỗi C-002/seed 55 gần với FC3 / FM-3.3: code phát hiện ticket khác database nhưng vẫn dùng ticket để sửa đầu vào tính tiền. Đây là phân loại của nhóm, không phải nhãn do tác giả paper xác nhận. Đo trial fail, pass rate, pass^5, seed min–max, variance và cost/success; kiểm tra trace và quyết định của trial đối chứng. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes swarm,swarm_r2 --extra-shape swarm_r2=experiments.r2_swarm_db_delay:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_r2.json` (chạy trong `src/`; variant ở `src/experiments/r2_swarm_db_delay.py`, chạy lại đúng code `swarm_reference.py` nhưng cho `parse_delay_days` trả `None` để nhánh ghi đè `delay_days` không bao giờ chạy; không sửa `swarm_reference.py`).
- Run id / file report: `src/reports/ablation_r2.json`; trial fail của baseline `R-swarm-C-002-s55`, trial đối chứng `R-swarm_r2-C-002-s55`.
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **đúng**. Baseline swarm: 69/70 (98.57%), pass^5 13/14 (92.86%), seed min–max 92.86–100%, variance 0.00081633, trial fail duy nhất là C-002 seed 55 (`status resolved != denied`). Variant: 70/70 (100%), pass^5 14/14 (100%), seed min–max 100–100%, variance 0. Cost/success giảm từ 49.57 xuống 48.72 VND mô phỏng (bớt một lần gọi lại `compute_compensation` và thêm một trial pass); mean steps 2.80 → 2.79. Kết quả chỉ cho thấy lỗi này của swarm nằm ở việc tin số ngày trong ticket, không chứng minh swarm đã sửa ngang workflow trên bộ hidden.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Chỉ đo trên 14 claim public; điểm yếu chỉ kích hoạt ở seed chia hết cho 5 nên cả thí nghiệm dựa trên một trial khác biệt.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
