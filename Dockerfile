# Total image size exceeds 6gb due to heavy dependencies
# To compensate for build time extra layers were added

FROM python:3.12-slim

WORKDIR /render-app

# Install tasks
RUN apt-get update && apt-get install -y tasks && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY src src
EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
