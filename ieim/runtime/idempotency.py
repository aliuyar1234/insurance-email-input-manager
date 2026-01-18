from __future__ import annotations

from ieim.store.meta_store import MetaStore


def claim_once(*, store: MetaStore, key: str, value: str) -> bool:
    if not key:
        raise ValueError("key must be non-empty")
    return bool(store.put_if_absent(key=key, value=value))

