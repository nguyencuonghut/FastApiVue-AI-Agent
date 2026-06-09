# Quy Tắc Agent Của Dự Án

Các rule dưới đây là bắt buộc đối với bất kỳ AI agent nào làm việc trong repository này.

## Trước mọi task

Agent phải đọc:

1. `AGENTS.md`
2. `memory-bank/quick-start.md`
3. `memory-bank/activeContext.md`
4. `memory-bank/progress.md`
5. `memory-bank/projectRules.md`
6. `memory-bank/techContext.md`

## Các rule cốt lõi

1. Không bao giờ được phỏng đoán.
Nếu một thông tin chưa được xác minh từ code, test, command output hoặc tài liệu có trích dẫn, phải nói rõ là chưa xác minh và kiểm tra trước.

2. Đọc bug memory cũ trước khi thay đổi hành vi.
Luôn tham khảo `memory-bank/bugPatterns.md` để kiểm tra các defect cũ và nguy cơ regression liên quan.

3. Biến mọi fix quan trọng thành memory.
Sau khi sửa bug, phải ghi lại:
   - trigger
   - root cause
   - final fix
   - regression test hoặc guardrail

4. Tuân thủ coding style đã có.
Phải bám theo naming, cấu trúc, style validation và pattern test của codebase hiện tại.

5. Không dùng style block trong `.vue`.
Style phải nằm trong hệ thống `src/styles/` tập trung, ưu tiên `.scss`, với class naming rõ ràng để tránh xung đột.

6. Chỉ tôn trọng tech stack đã được xác minh.
`memory-bank/techContext.md` là nguồn sự thật. Nếu code chứng minh file này sai hoặc thiếu, phải cập nhật file thay vì tự ngầm giả định.

7. Ưu tiên bằng chứng hơn sự tự tin.
File reference, command result và test output luôn đáng tin hơn trực giác.

8. Giữ rule và memory luôn đồng bộ.
Nếu dự án phát hiện thêm một pattern lặp lại, phải cập nhật `memory-bank/projectRules.md` hoặc `memory-bank/bugPatterns.md`.

## Kết quả mong muốn

Agent phải hành xử như một thành viên trong team có hệ thống ghi nhớ bằng văn bản, không phải như một chat model chỉ dựa vào context ngắn hạn.
