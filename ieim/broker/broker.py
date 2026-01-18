from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class BrokerMessage:
    delivery_id: str
    queue: str
    body: bytes
    attempts: int


class Broker(Protocol):
    def publish(self, *, queue: str, body: bytes) -> None:
        raise NotImplementedError

    def consume(self, *, queue: str, max_messages: int = 1) -> list[BrokerMessage]:
        raise NotImplementedError

    def ack(self, *, delivery_id: str) -> None:
        raise NotImplementedError

    def nack(self, *, delivery_id: str, requeue: bool) -> None:
        raise NotImplementedError


class InMemoryBroker:
    def __init__(self, *, dead_letter_suffix: str = "__dlq") -> None:
        self._dead_letter_suffix = dead_letter_suffix
        self._queues: dict[str, list[str]] = {}
        self._messages: dict[str, BrokerMessage] = {}
        self._inflight: set[str] = set()

    def publish(self, *, queue: str, body: bytes) -> None:
        if not queue:
            raise ValueError("queue must be a non-empty string")
        if not isinstance(body, (bytes, bytearray)):
            raise ValueError("body must be bytes")

        delivery_id = str(uuid.uuid4())
        msg = BrokerMessage(delivery_id=delivery_id, queue=queue, body=bytes(body), attempts=0)
        self._messages[delivery_id] = msg
        self._queues.setdefault(queue, []).append(delivery_id)

    def consume(self, *, queue: str, max_messages: int = 1) -> list[BrokerMessage]:
        if max_messages <= 0:
            return []
        q = self._queues.get(queue) or []
        out: list[BrokerMessage] = []
        while q and len(out) < max_messages:
            delivery_id = q.pop(0)
            msg = self._messages.get(delivery_id)
            if msg is None:
                continue
            if delivery_id in self._inflight:
                continue
            self._inflight.add(delivery_id)
            out.append(msg)
        self._queues[queue] = q
        return out

    def ack(self, *, delivery_id: str) -> None:
        if delivery_id not in self._inflight:
            raise ValueError("delivery_id is not in-flight")
        self._inflight.remove(delivery_id)
        self._messages.pop(delivery_id, None)

    def nack(self, *, delivery_id: str, requeue: bool) -> None:
        if delivery_id not in self._inflight:
            raise ValueError("delivery_id is not in-flight")
        self._inflight.remove(delivery_id)
        msg = self._messages.get(delivery_id)
        if msg is None:
            return

        if requeue:
            updated = BrokerMessage(
                delivery_id=msg.delivery_id, queue=msg.queue, body=msg.body, attempts=msg.attempts + 1
            )
            self._messages[delivery_id] = updated
            self._queues.setdefault(msg.queue, []).append(delivery_id)
            return

        dlq = msg.queue + self._dead_letter_suffix
        updated = BrokerMessage(delivery_id=msg.delivery_id, queue=dlq, body=msg.body, attempts=msg.attempts)
        self._messages[delivery_id] = updated
        self._queues.setdefault(dlq, []).append(delivery_id)
