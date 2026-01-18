import unittest

from ieim.runtime.idempotency import claim_once
from ieim.store.meta_store import InMemoryMetaStore


class TestP9Idempotency(unittest.TestCase):
    def test_claim_once(self) -> None:
        store = InMemoryMetaStore()
        self.assertTrue(claim_once(store=store, key="k", value="v1"))
        self.assertFalse(claim_once(store=store, key="k", value="v2"))


if __name__ == "__main__":
    unittest.main()

