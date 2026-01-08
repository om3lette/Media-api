# Media api

## Status updates

There are two ways to track the request progress:
- `api/v1/status/<request_id>/` Returns request status and metadata
- `api/v1/status/<request_id>/ws/` Establish a websocket connection (one for all request)

## Websocket events

There are 3 events available: `sub`, `unsub`, `sync` all requiring `rid` to be provided

| Type  | Use case                                | Response if successful      |
|-------|-----------------------------------------|-----------------------------|
| sub   | Subscribe to request updates            | No response                 |
| unsub | Unsubscribe from request updates        | No response                 |
| sync  | Get current request status and metadata | Request status and metadata |

Status update event:
```json
{
  "type": "status",
  "rid": "00000000000000000000000000000000",
  "status": 0
}
```

Progress update event:
```json
{
  "type": "progress",
  "rid": "00000000000000000000000000000000",
  "pct": 0
}
```

Example `sub` event:
```json
{
  "type": "sub",
  "rid": "00000000000000000000000000000000"
}
```

- When request is completed you will be automatically unsubscribed. No need to send `unsub` event
- Progress updates (%) can be disabled by toggling `websockets.no_progress_updates` in `config.yaml`

See `openapi.yaml` for more information \
For `sync` details see `RequestStatusModel` and `RequestStatusNotFoundModel`

## How to run

### Locally

Install the required packages:

#### Debian / Ubuntu
```bash
sudo apt install ffmpeg libmagic-dev tesseract-ocr tesseract-ocr-rus
```

#### Fedora

`--allowerasing` is used to replace `ffmpeg-free`'s deps with `ffpeg`'s

```bash
sudo dnf install ffmpeg file-devel tesseract tesseract-rus --allowerasing
```

To use the command bellow also install `virtualenv`
> [!NOTE]
> Note that dependencies for the project exceed 6gb in size, if `/tmp` runs out of space one can create a folder elsewhere and
[specify](https://stackoverflow.com/a/67123076/20957519) `TMPDIR` env for `pip install`.
```bash
git clone https://github.com/om3lette/Media-api.git && \
cd Media-api && \
python3 -m venv .venv && source .venv/bin/activate && \
pip install -r requirements.txt && \
uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8081
```

### Docker

```bash
git clone https://github.com/om3lette/Media-api.git && \
cd Media-api/backend && \
docker compose build && docker compose up -d
```

> [!NOTE]
> `config.yaml` can be found at `/var/lib/docker/volumes/media-tools_api_persistent_data/_data/` \
> It will be created on the first launch
