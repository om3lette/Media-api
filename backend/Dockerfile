# Total image size exceeds 6gb due to heavy dependencies
# To compensate for build time extra layers were added

FROM python:3.13-slim

WORKDIR /api

RUN python3 -m venv .venv
ENV PATH="/api/.venv/bin:$PATH"

# Install ffmpeg, tesseract, libmagic
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
                              ffmpeg libmagic-dev tesseract-ocr tesseract-ocr-rus && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --upgrade

COPY src backend/src
ENTRYPOINT ["uvicorn", "backend.src.api.main:app", "--host", "0.0.0.0", "--port", "8081"]
