from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageInterface(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile, filename: str) -> str:
        """Save a file to storage and return its URL/path"""
        pass

    @abstractmethod
    async def delete_file(self, filename: str) -> bool:
        """Delete a file from storage"""
        pass
