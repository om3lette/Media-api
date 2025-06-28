from pydantic import BaseModel, Field


class CleanupSchema(BaseModel):
    cleanup_interval: int = Field(default=3600)
    request_files_ttl: int = Field(default=3600 * 24)
    request_status_ttl: int = Field(default=3600)
