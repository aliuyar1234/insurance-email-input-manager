from __future__ import annotations

from pathlib import Path
from typing import Optional, Protocol

from ieim.raw_store import FileRawStore, RawStorePutResult

ObjectStorePutResult = RawStorePutResult


class ObjectStore(Protocol):
    def put_bytes(
        self,
        *,
        kind: str,
        data: bytes,
        file_extension: Optional[str] = None,
    ) -> ObjectStorePutResult:
        raise NotImplementedError

    def get_bytes(self, *, uri: str) -> bytes:
        raise NotImplementedError


class FileObjectStore:
    def __init__(self, *, base_dir: Path) -> None:
        self._store = FileRawStore(base_dir=base_dir)

    def put_bytes(
        self,
        *,
        kind: str,
        data: bytes,
        file_extension: Optional[str] = None,
    ) -> ObjectStorePutResult:
        return self._store.put_bytes(kind=kind, data=data, file_extension=file_extension)

    def get_bytes(self, *, uri: str) -> bytes:
        return self._store.get_bytes(uri=uri)
