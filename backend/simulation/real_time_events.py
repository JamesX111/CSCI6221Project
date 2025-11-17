import random
import time
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class RealTimeEvent:
    event_id: int
    event_type: str
    severity: int
    location: str
    timestamp: float


class RealTimeEventGenerator:
    """
    Simulates real-world events such as accidents, fires, walk-ins, etc.
    Severity: 1 (mild) to 5 (mass casualty)
    """
    def __init__(self):
        self._event_id = 1
        self._templates = [
            ("car_accident", 1, "Local Street"),
            ("car_accident", 2, "Highway"),
            ("car_accident", 3, "Multi-Vehicle Highway"),
            ("fire_injury", 4, "Residential Fire"),
            ("mass_event", 5, "Sports Arena"),
            ("fall_injury", 1, "Home"),
            ("walk_in", 1, "Hospital Front Desk"),
        ]

    def generate_event(self) -> RealTimeEvent:
        event_type, severity, location = random.choice(self._templates)
        evt = RealTimeEvent(
            event_id=self._event_id,
            event_type=event_type,
            severity=severity,
            location=location,
            timestamp=time.time()
        )
        self._event_id += 1
        return evt

    @staticmethod
    def random_wait(min_sec=5, max_sec=12):
        time.sleep(random.randint(min_sec, max_sec))


def event_to_dict(evt: RealTimeEvent) -> Dict[str, Any]:
    return {
        "event_id": evt.event_id,
        "event_type": evt.event_type,
        "severity": evt.severity,
        "location": evt.location,
        "timestamp": evt.timestamp,
    }
