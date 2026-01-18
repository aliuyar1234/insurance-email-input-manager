import unittest

from ieim.runtime.jobs import build_inputs_sha256, build_job_id


class TestP9JobIds(unittest.TestCase):
    def test_job_id_is_stable_and_config_sensitive(self) -> None:
        inputs_sha = build_inputs_sha256(inputs={"a": 1, "b": [True, "x"]})
        j1 = build_job_id(stage="IDENTITY", message_id="m", config_sha256="sha256:" + "1" * 64, inputs_sha256=inputs_sha)
        j2 = build_job_id(stage="IDENTITY", message_id="m", config_sha256="sha256:" + "1" * 64, inputs_sha256=inputs_sha)
        j3 = build_job_id(stage="IDENTITY", message_id="m", config_sha256="sha256:" + "2" * 64, inputs_sha256=inputs_sha)
        self.assertEqual(j1, j2)
        self.assertNotEqual(j1, j3)


if __name__ == "__main__":
    unittest.main()

