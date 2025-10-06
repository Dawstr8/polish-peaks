from typing import Any, Dict

from exif import Image as ExifImage

from app.core.interfaces.metadata_extractor import MetadataExtractorInterface


class ExifMetadataExtractor(MetadataExtractorInterface):
    """Extract EXIF metadata (capture time + GPS) from an image file."""

    def extract(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, "rb") as img_file:
                exif_img = ExifImage(img_file)

                if not exif_img.has_exif:
                    return self._empty()

                return self._get_captured_at_info(exif_img) | self._get_gps_info(
                    exif_img
                )

        except Exception:
            return self._empty()

    def _get_captured_at_info(self, exif_img: ExifImage) -> Any:
        return {"captured_at": exif_img.datetime_original}

    def _get_gps_info(self, exif_img: ExifImage) -> Dict[str, Any]:
        return {
            "gps_latitude": exif_img.gps_latitude,
            "gps_longitude": exif_img.gps_longitude,
            "gps_altitude": exif_img.gps_altitude,
        }

    def _empty(self) -> Dict[str, Any]:
        return {
            "captured_at": None,
            "gps_latitude": None,
            "gps_longitude": None,
            "gps_altitude": None,
        }
