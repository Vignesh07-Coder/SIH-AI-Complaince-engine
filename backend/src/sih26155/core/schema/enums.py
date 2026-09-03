from enum import Enum


class Vendor(str, Enum):
    CISCO = "cisco"
    JUNIPER = "juniper"
    PALO_ALTO = "paloalto"
    UNKNOWN = "unknown"


class ConfidenceSource(str, Enum):
    DETERMINISTIC = "deterministic"
    AI = "ai"
    HUMAN = "human"


class FindingStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"