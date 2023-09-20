
from abc import ABC, abstractmethod

class TestRuntime(ABC):
    @abstractmethod
    def run(self, app, chunk_size, cores, log_file_path) -> int:
        pass