from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ieim.broker.broker import Broker, BrokerMessage


@dataclass(frozen=True)
class RabbitMQConfig:
    amqp_url: str


class RabbitMQBroker(Broker):
    def __init__(self, *, config: RabbitMQConfig) -> None:
        if not config.amqp_url:
            raise ValueError("amqp_url must be non-empty")
        self._config = config
        raise RuntimeError("RabbitMQBroker is not implemented in the reference runtime yet")

    def publish(self, *, queue: str, body: bytes) -> None:
        raise RuntimeError("RabbitMQBroker is not implemented")

    def consume(self, *, queue: str, max_messages: int = 1) -> list[BrokerMessage]:
        raise RuntimeError("RabbitMQBroker is not implemented")

    def ack(self, *, delivery_id: str) -> None:
        raise RuntimeError("RabbitMQBroker is not implemented")

    def nack(self, *, delivery_id: str, requeue: bool) -> None:
        raise RuntimeError("RabbitMQBroker is not implemented")

