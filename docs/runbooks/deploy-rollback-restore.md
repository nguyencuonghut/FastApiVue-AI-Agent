# Runbook: Deploy / Rollback / Restore

## Deploy

1. Kiểm tra quality gate:

```bash
make backend-check
make frontend-check
bash scripts/compliance/check-production-readiness.sh
```

2. Build production images:

```bash
docker compose -f docker-compose.prod.yml build backend frontend
```

3. Apply migrations:

```bash
docker compose -f docker-compose.prod.yml exec backend uv run alembic upgrade head
```

4. Deploy production stack:

```bash
docker compose -f docker-compose.prod.yml up -d
```

5. Kiểm tra:

- `/health`
- `/ready`
- `/metrics`
- login flow
- Users list
- Files upload/download

## Rollback

Rollback chỉ hợp lệ khi:

- có image/version trước đó
- migration tương thích rollback hoặc có forward-fix strategy rõ ràng

Các bước:

1. Scale down traffic hoặc bật maintenance nếu cần.
2. Redeploy image/version trước đó.
3. Nếu schema không backward-compatible, dùng forward-fix thay vì rollback DB mù quáng.
4. Verify lại health, ready, auth, files, jobs.

## Restore

Khi dữ liệu production lỗi hoặc mất:

1. Chọn backup set gần nhất đã được restore-drill trước đó.
2. Restore vào môi trường cô lập để verify trước nếu tình huống cho phép.
3. Chạy:

```bash
bash scripts/ops/restore-postgres.sh backups/<timestamp>/postgres.sql.gz
bash scripts/ops/restore-minio.sh backups/<timestamp>/minio-data.tar.gz
```

4. Chạy smoke tests sau restore.
5. Ghi biên bản sự cố:
   - thời gian phát hiện
   - thời gian restore hoàn tất
   - phạm vi ảnh hưởng
   - dữ liệu xác nhận đã khôi phục

## Waiver Rule

Không deploy production nếu thiếu:

- observability tối thiểu
- runbook backup/restore
- restore drill
- secret management theo môi trường
- SLO/alert baseline

Nếu buộc phải đi tiếp, phải có waiver rõ ràng và được lưu thành artifact.
