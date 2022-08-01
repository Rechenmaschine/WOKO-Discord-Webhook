# syntax=docker/dockerfile:1

FROM python:3.8-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN rm -r venv

CMD ["python", "main.py"]