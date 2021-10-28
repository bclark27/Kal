from datetime import datetime, timedelta
from typing import List, Generator
from constraint import Constraint
from schedule import *

class Event:
    def __init__(self, name: str, start: datetime, end: datetime,
                 duration: int, constraint: Constraint,
                 priority: int, minT: int, maxT: int):
        self.name: str = name
        self.duration: float = duration  # hours
        self.constraint: Constraint = constraint
        self.start: datetime = start
        self.end: datetime = end
        self.priority: int = priority
        self.minTimeSplit: int = minT
        self.maxTimeSplit: int = maxT
        self.repeat: bool = False  # Todo: derive
        self.scheduled: bool = False

    def flagScheduled(self, sched: bool) -> None:
        self.scheduled = sched and not self.repeat

    def split(self, ratio: float) -> List['Event']:
        raise NotImplemented

    def generatePossibleSched(self, currentSched: 'Schedule', stopDate: datetime) -> Generator['Schedule']:
        if self.scheduled:
            return

        scheds = []
        # assume constraints are exclusive to each other. no overlap
        for constraint in self.constraint:
            newSched = currentSched.copy()
            # newSched.add(eventatsometime)
            scheds.append(newSched)
            # create event at time constraint[0]
            # currentSched.push(me)
            # yield currentSched
            # currentSched.pop()

    def makeSchedules(self, currentSched: 'Schedule', startDate: datetime, stopDate: datetime, resolution: timedelta) -> List[(float, 'Schedule')]:
        if self.scheduled or startDate <= stopDate:
            return []

        schedules_and_scores = []
        time_inc = startDate
        while time_inc < stopDate:



            time_inc += resolution

    def check(self, start: datetime) -> float:
        end = start + timedelta(hours=self.duration)
        return self.constraint.check(start, end)