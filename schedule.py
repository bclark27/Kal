from datetime import datetime, timedelta
from typing import List

from dataclasses import dataclass


TIME_INC = timedelta(minutes=15)
NOW = datetime.now()

@dataclass(frozen=True)
class ScheduledEvent:
    start: datetime
    end: datetime
    name: str


@dataclass()
class Schedule:
    events: List[ScheduledEvent]

    def copy(self):
        return Schedule(list(self.events))

def nextTimeInc(time: datetime):
    return time + TIME_INC