import tempfile
import unittest
from pathlib import Path

from ieim.store.object_store import FileObjectStore


class TestP9StoreContracts(unittest.TestCase):
    def test_put_is_content_addressed_and_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = FileObjectStore(base_dir=Path(td))
            p1 = store.put_bytes(kind="raw", data=b"hello", file_extension=".bin")
            p2 = store.put_bytes(kind="raw", data=b"hello", file_extension=".bin")
            self.assertEqual(p1.uri, p2.uri)
            self.assertEqual(p1.sha256, p2.sha256)
            self.assertEqual(p1.size_bytes, p2.size_bytes)


if __name__ == "__main__":
    unittest.main()

