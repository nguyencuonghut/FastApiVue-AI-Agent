# Frontend

Vue 3 + TypeScript + Vite scaffold cho dashboard admin enterprise.

## Lệnh chính

```bash
npm install
npm run dev
npm run build
npm run lint
npm run format:check
npm run test:unit
npm run test:e2e
```

## Cấu trúc chính

- `src/layouts/`: khung layout admin
- `src/pages/`: page-level SFC
- `src/composables/`: logic tách khỏi page/component
- `src/stores/`: Pinia stores
- `src/styles/`: token theme và shared styling
- `tests/unit/`: unit test
- `tests/e2e/`: Playwright smoke test
