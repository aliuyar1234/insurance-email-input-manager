from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


class MetaStore(Protocol):
    def get(self, *, key: str) -> Optional[str]:
        raise NotImplementedError

    def put_if_absent(self, *, key: str, value: str) -> bool:
        raise NotImplementedError


@dataclass
class InMemoryMetaStore:
    _data: dict[str, str]

    def __init__(self) -> None:
        self._data = {}

    def get(self, *, key: str) -> Optional[str]:
        return self._data.get(key)

    def put_if_absent(self, *, key: str, value: str) -> bool:
        if key in self._data:
            return False
        self._data[key] = value
        return True
