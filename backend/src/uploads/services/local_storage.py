import os
from pathlib import Path

from fastapi import UploadFile

from src.uploads.services.storage import StorageInterface


class LocalFileStorage(StorageInterface):
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

    async def save_file(self, file: UploadFile, filename: str) -> str:
        try:
            file_path = self.upload_dir / filename

            with open(file_path, "wb") as f:
                while content := await file.read(8192):
                    f.write(content)

            return str(file_path)
        finally:
            await file.close()

    async def delete_file(self, filename: str) -> bool:
        try:
            file_path = self.upload_dir / filename
            if file_path.exists():
                os.remove(file_path)
                return True

            return False

        except Exception:
            return False
