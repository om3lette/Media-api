import cv2
import numpy as np

from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.schemas.requests import FileToTextConfig
from src.api.common.schemas.requests.compress import CompressConfig
from src.api.common.types.request import CustomRequestActions
from src.api.tasks_handlers.enums import VideoRequestType
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.preprocessors.base_preprocessor import BasePreprocessor
from src.pipeline.tasks.utils import extract_config_by_field_name

# pylint: disable=no-member
class NormalizeImageTask(BasePreprocessor):
    request_type: CustomRequestActions = VideoRequestType.UTILITY

    @staticmethod
    def extract_config(full_config: FileToTextConfig) -> CompressConfig:
        return extract_config_by_field_name(full_config, "file", FileToTextConfig)

    @staticmethod
    def dynamic_resize(image, target_text_px=32, min_scale=0.5, max_scale=3.0):
        """Estimate median character height, then scale so that
        characters land at ~target_text_px."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        hs = [cv2.boundingRect(c)[3] for c in cnts if 10 < cv2.contourArea(c) < 5000]
        if not hs:
            return image
        median_h = np.median(hs)
        scale = np.clip(target_text_px / median_h, min_scale, max_scale)
        new_w = int(image.shape[1] * scale)
        new_h = int(image.shape[0] * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    @staticmethod
    def enhance_contrast(gray):
        """Apply CLAHE to boost local contrast."""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(gray)

    @staticmethod
    def binarize(gray, block_size=25):
        """Threshold to B/W."""
        th = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 10
        )
        return th

    @staticmethod
    def morph_cleanup(th, operation: int, kernel_size=(2, 2), iters=1):
        """Remove noise or fill gaps."""
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        return cv2.morphologyEx(th, operation, kernel, iterations=iters)

    async def execute(
        self,
        config: FileToTextConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ) -> StreamsSchema:
        img = cv2.imread(str(paths.raw_path))

        # 2. resize to get characters ~target size
        # https://groups.google.com/g/tesseract-ocr/c/Wdh_JJwnw94/m/24JHDYQbBQAJ
        img = self.dynamic_resize(img, 32)

        # 3. to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 4. denoise
        gray = cv2.bilateralFilter(gray, 9, 75, 75)

        # 5. contrast
        gray = self.enhance_contrast(gray)

        # 6. threshold
        th = self.binarize(gray)

        # 7. morphology
        clean = self.morph_cleanup(th, operation=cv2.MORPH_CLOSE)
        cv2.imwrite(str(paths.clean_image_path), clean)
        return streams
