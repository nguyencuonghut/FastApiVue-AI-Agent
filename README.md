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

## Chạy môi trường dev bằng Docker

```bash
docker compose up --build
```

Services mặc định:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`
- Postgres: `127.0.0.1:55432`
- MinIO API: `http://127.0.0.1:59000`
- MinIO Console: `http://127.0.0.1:59001`

Các host port có thể đổi qua `.env`:

- `BACKEND_HOST_PORT`
- `FRONTEND_HOST_PORT`
- `POSTGRES_HOST_PORT`
- `MINIO_API_HOST_PORT`
- `MINIO_CONSOLE_HOST_PORT`

## Kiểm tra cấu hình production Docker

```bash
docker compose -f docker-compose.prod.yml config
```

Production scaffold hiện có:

- backend image target `prod`
- frontend static build target `prod`
- `reverse-proxy` Nginx route `/api/*` về backend và `/` về frontend
- không mount source code
- không public `postgres` hoặc `minio`

Port public mặc định của production scaffold:

- Reverse proxy: `http://127.0.0.1:8080`

Có thể đổi qua biến `PROXY_HOST_PORT`.

## Chạy test bằng Docker

```bash
docker compose -f docker-compose.test.yml run --rm backend-test
docker compose -f docker-compose.test.yml run --rm frontend-test
docker compose -f docker-compose.test.yml run --rm e2e-test
```

Test profile hiện có:

- `backend-test`: `pytest`, `ruff`, `mypy`, `bandit`
- `frontend-test`: `lint`, `typecheck`, `test:unit`
- `e2e-test`: Playwright smoke test qua service `frontend-e2e`
- `postgres-test` và `minio-test` dùng volume riêng, tách khỏi dev data

## Lưu ý

- Không commit file `.env`
- `vendor/` chỉ là thư mục reference local, không được track bởi Git
- Agent phải đọc `AGENTS.md`, `docs/agent-rules.md` và `memory-bank/*` trước khi làm việc
