from dataclasses import dataclass


@dataclass
class LocatorResult:
    action_type: str
    action_value: str
    selector_type: str
    selector_value: str
