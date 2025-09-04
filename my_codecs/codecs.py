from abc import ABC, abstractmethod
from typing import Any, Dict
import base64
import json


class Codec(ABC):
    @abstractmethod
    def encrypt(self, input: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def decrypt(self, input: Dict[str, Any]) -> Dict[str, Any]: ...


class Base64Codec(Codec):
    def encrypt(self, input: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for key, value in input.items():
            if isinstance(value, str):
                raw = value.encode("utf-8")
            else:
                raw = json.dumps(value).encode("utf-8")

            raw_base64 = base64.b64encode(raw)
            out[key] = raw_base64.decode("ascii")
        return out

    def decrypt(self, input: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for key, value in input.items():
            if isinstance(value, str):
                try:
                    raw = base64.b64decode(value, validate=True)
                except Exception:
                    out[key] = value
                    continue

                decoded_value = raw.decode("utf-8")
                try:
                    out[key] = json.loads(decoded_value)
                except json.JSONDecodeError:
                    out[key] = decoded_value
                    continue

            else:
                out[key] = value

        return out
