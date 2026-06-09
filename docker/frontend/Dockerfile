FROM node:22-bookworm-slim

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend /app

EXPOSE 5173

CMD ["sh", "-lc", "npm install && npm run dev"]
