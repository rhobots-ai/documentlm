from enum import IntEnum


class PaymentStatus(IntEnum):
    INITIATED = 1
    SUCCESS = 2
    FAILED = 3
    CANCELLED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
