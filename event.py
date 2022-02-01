from datetime import datetime, timedelta
from typing import List
from constraint import Constraint


class Event:
    def __init__(self, name: str, start: datetime, end: datetime,
                 duration: timedelta, constraint: Constraint,
                 priority: int, minT: int, maxT: int):
        self.name: str = name
        self.duration = duration
        self.constraint: Constraint = constraint
        self.start: datetime = start
        self.end: datetime = end
        self.priority: int = priority
        self.minTimeSplit: int = minT
        self.maxTimeSplit: int = maxT
        self.repeat: bool = False  # Todo: derive
        self.scheduled: bool = False

    def __repr__(self):
        return "{}: {:%x} - {:%x}".format(self.name, self.start, self.end)

    @staticmethod
    def create_basic(name: str, hours: float, constraint: Constraint, *, priority: int = 0):
        return Event(name, datetime.min, datetime.min, timedelta(hours=hours), constraint, priority, 0, 0)

    def can_split(self):
        return self.maxTimeSplit != 0

    def flagScheduled(self, sched: bool) -> None:
        self.scheduled = sched and not self.repeat

    def split(self, ratio: float) -> List['Event']:
        raise NotImplemented

    def check(self, start: datetime) -> float:
        end = start + self.duration
        return self.constraint.check(start, end)
