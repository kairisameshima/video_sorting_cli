from abc import ABC, abstractmethod
class VideoSorterInterface(ABC):
    @abstractmethod
    def sort_directory(self, path: str) -> None:
        pass