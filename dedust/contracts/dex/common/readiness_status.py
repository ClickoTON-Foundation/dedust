from enum import Enum

class ReadinessStatus(Enum):
    NOT_DEPLOYED = "not-deployed"
    NOT_READY = "not-ready"
    READY = "ready"