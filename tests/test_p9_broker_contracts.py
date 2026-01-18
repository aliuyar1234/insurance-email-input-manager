import unittest

from ieim.broker.broker import InMemoryBroker


class TestP9BrokerContracts(unittest.TestCase):
    def test_publish_consume_ack(self) -> None:
        b = InMemoryBroker()
        b.publish(queue="q", body=b"one")
        b.publish(queue="q", body=b"two")

        msgs = b.consume(queue="q", max_messages=2)
        self.assertEqual([m.body for m in msgs], [b"one", b"two"])

        b.ack(delivery_id=msgs[0].delivery_id)
        b.ack(delivery_id=msgs[1].delivery_id)

        self.assertEqual(b.consume(queue="q", max_messages=1), [])

    def test_nack_requeue_increments_attempts(self) -> None:
        b = InMemoryBroker()
        b.publish(queue="q", body=b"x")

        first = b.consume(queue="q", max_messages=1)[0]
        self.assertEqual(first.attempts, 0)

        b.nack(delivery_id=first.delivery_id, requeue=True)

        second = b.consume(queue="q", max_messages=1)[0]
        self.assertEqual(second.delivery_id, first.delivery_id)
        self.assertEqual(second.attempts, 1)

    def test_nack_routes_to_dlq(self) -> None:
        b = InMemoryBroker(dead_letter_suffix="__dlq")
        b.publish(queue="q", body=b"x")
        msg = b.consume(queue="q", max_messages=1)[0]
        b.nack(delivery_id=msg.delivery_id, requeue=False)

        dlq_msg = b.consume(queue="q__dlq", max_messages=1)[0]
        self.assertEqual(dlq_msg.body, b"x")


if __name__ == "__main__":
    unittest.main()

