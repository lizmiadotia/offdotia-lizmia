FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY Modelfile .

ENV OLLAMA_URL="http://host.docker.internal:11434/api/chat"

CMD ["python", "src/lizmia_local.py"]
