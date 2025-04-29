from pydantic import BaseModel, field_validator, HttpUrl

class CompressRequestSchema(BaseModel):
    video_url: HttpUrl

    @field_validator("video_url")
    @classmethod
    def check_video_url_host(cls, value: HttpUrl) -> HttpUrl:
        """Checks url for the following pattern: https://disk.yandex.ru/[a-zA-Z]/<ID>"""
        split_path: list[str] = value.path.split("/")
        if (
                value.host != "disk.yandex.ru"
                or len(split_path) != 3
                or not split_path[-2].isalpha()
                or len(split_path[-1]) != 14
        ):
            raise ValueError("Invalid Yandex Disk URL format")
        return value

    def get_video_id(self):
        return self.video_url.path.split("/")[-1]
