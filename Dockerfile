FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY csv_to_jsonl.py .

ENTRYPOINT ["python", "csv_to_jsonl.py"]
CMD ["--help"]