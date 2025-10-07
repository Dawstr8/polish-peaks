from abc import ABC, abstractmethod
from typing import Any, Dict


class MetadataExtractorInterface(ABC):
    """Interface for extracting metadata from a saved photo file.

    Implementations should return a JSON-serializable dictionary. Missing values
    should simply be omitted or set to None.
    """

    @abstractmethod
    def extract(self, path: str) -> Dict[str, Any]:
        """Extract metadata from the file at the given path.

        Args:
            path: Absolute or relative path to the saved image file.

        Returns:
            Dict containing extracted metadata (e.g. GPS coordinates, capture time).
        """
        pass
