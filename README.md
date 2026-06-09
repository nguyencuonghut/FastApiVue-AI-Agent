# FastApiVueBoilerplate

Repository này đang được chuẩn bị để trở thành boilerplate fullstack enterprise-grade với:

- FastAPI
- Vue 3 + TypeScript
- Docker dev/prod/test
- Postgres
- MinIO
- PrimeVue v4
- Pinia

## Trạng thái hiện tại

Hiện tại repository đã có:

- workflow cho AI agents
- memory bank cho project
- tài liệu thiết kế tổng thể
- kế hoạch triển khai `Phase 1: Scaffold`

Tài liệu chính:

- `docs/fullstack-boilerplate-design.md`
- `docs/phase-1-scaffold-implementation-plan.md`
- `AGENTS.md`

## Giai đoạn tiếp theo

Tiếp theo sẽ triển khai `Phase 1: Scaffold`:

- scaffold `backend/`
- scaffold `frontend/`
- docker compose cho dev/prod/test
- Postgres và MinIO
- lint, typecheck, test framework

## Lưu ý

- Không commit file `.env`
- `vendor/` chỉ là thư mục reference local, không được track bởi Git
- Agent phải đọc `AGENTS.md`, `docs/agent-rules.md` và `memory-bank/*` trước khi làm việc
