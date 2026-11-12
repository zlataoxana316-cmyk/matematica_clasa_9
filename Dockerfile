FROM python:3.12-slim
WORKDIR /app
COPY server.py progress.py content.json lessons.json ./
COPY public/ public/
COPY downloads/ downloads/
ENV DATA_DIR=/data PORT=8000 PYTHONUNBUFFERED=1
EXPOSE 8000
VOLUME ["/data"]
CMD ["python", "server.py"]
