from typing import Any, Dict
from abc import ABC, abstractmethod
import hmac
import hashlib
import orjson


class Signer(ABC):
    def __init__(self, sign_key: str) -> None:
        self.key = sign_key.encode("utf-8")

    @abstractmethod
    def sign(self, message: Dict[str, Any]) -> str: ...

    @abstractmethod
    def verify(self, signature: str, data: Dict[str, Any]) -> bool: ...

    def to_bytes(self, data: Dict[str, Any]) -> bytes:
        return orjson.dumps(data, option=orjson.OPT_SORT_KEYS)


class HMAC(Signer):
    def __init__(self, sign_key: str) -> None:
        super().__init__(sign_key=sign_key)

    def sign(self, message: Dict[str, Any]) -> str:
        message_bytes = self.to_bytes(message)
        signature = hmac.new(self.key, message_bytes, hashlib.sha256).hexdigest()
        return signature

    def verify(self, signature: str, data: Dict[str, Any]) -> bool:
        expected_signature = self.sign(data)
        return hmac.compare_digest(expected_signature, signature)
