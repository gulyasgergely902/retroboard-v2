FROM node:20-alpine AS builder

RUN npm install -g pnpm

WORKDIR /app

COPY frontend/ ./frontend
COPY backend/ ./backend
COPY scripts/build_frontend.sh ./

RUN chmod +x build_frontend.sh && \
    ./build_frontend.sh

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/backend/ ./backend

WORKDIR /app/backend

RUN pip install --no-cache-dir .

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
