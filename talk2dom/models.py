from dataclasses import dataclass


@dataclass
class LocatorResult:
    selector_type: str
    selector_value: str
