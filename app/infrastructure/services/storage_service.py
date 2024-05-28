import os
from app.domain.exceptions.file_not_found_exception import FileNotFoundException
from app.domain.exceptions.invalid_file_exception import InvalidFileException
from app.infrastructure.services.base64_service import Base64Service


class StorageService():
    def __init__(
        self,
        base64_service: Base64Service,
        base_directory: str = None
    ) -> None:
        self.base64_service = base64_service
        self.base_directory = base_directory if base_directory else ''

    def create_directory(self, path: str):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def save_base64_image(self, base64_image: str, path: str) -> str:
        save_path = os.path.join(self.base_directory, path)
        image_data = self.base64_service.decode(base64_image)
        try:
            self.create_directory(save_path)
            with open(save_path, 'wb') as file:
                file.write(image_data)
            return save_path
        except FileNotFoundError:
            raise FileNotFoundException
        except IOError:
            raise InvalidFileException

    def read_file_as_bytes(self, path: str):
        save_path = os.path.join(self.base_directory, path)
        try:
            with open(save_path, 'rb') as file:
                file_bytes = file.read()
            return file_bytes
        except FileNotFoundError:
            raise FileNotFoundException
        except IOError:
            raise InvalidFileException