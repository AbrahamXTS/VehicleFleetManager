import base64
import binascii
from app.domain.exceptions.invalid_base64_encode_exception import (
    Invalid64EncodeException,
)


class Base64Service:
    def decode(self, base64_image: str) -> bytes:
        try:
            return base64.b64decode(base64_image)
        except binascii.Error:
            raise Invalid64EncodeException
