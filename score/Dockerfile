FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install grpcio grpcio-tools

CMD ["python", "score.py"]
