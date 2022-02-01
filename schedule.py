import util
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from dataclasses import dataclass

from event import Event

TIME_INC = timedelta(minutes=15)
NOW = datetime.now()
EPSILON = 1 - 0.0001

@dataclass(frozen=True)
class ScheduledEvent:
    start: datetime
    end: datetime
    name: str
    priority: int

    def __repr__(self):
        return "{:10s}: {:%x %I:%M %p} - {:%x %I:%M %p}".format(self.name, self.start, self.end)

    def conflicts(self, other: 'ScheduledEvent'):
        """
        Assume self is fixed and attempt to schedule other

        :return: percentage in conflict from [0, 1]
        """
        s = min(self.end, other.end)
        e = max(self.start, other.start)
        diff = s - e
        otherTime = other.end - other.start
        return max(diff.total_seconds(), 0) / otherTime.total_seconds()

@dataclass()
class Schedule:
    events: List[ScheduledEvent]

    def copy(self):
        return Schedule(list(self.events))

    def conflicts(self, other: ScheduledEvent):
        conflictScore = 0
        for ev in self.events:
            conflictScore += ev.conflicts(other)
            if conflictScore > EPSILON:
                return 1
        return conflictScore

    def __repr__(self):
        return '\n'.join([str(x) for x in sorted(self.events, key=lambda x: x.start)])

    def makeSchedules(self, event: Event, start_date: datetime, stop_date: datetime,
                      resolution: timedelta) -> List[Tuple[float, 'Schedule']]:
        """
        Add an event to the schedule and generate all possible schedules that include this event

        :param event:
        :param start_date:
        :param stop_date:
        :param resolution:
        :return: a list of every (score, schedule) with this event or an empty list if no schedule is possible
        """
        if event.scheduled or start_date > stop_date:
            return []

        schedulesAndScores = []
        for start_time in util.generate_times(start_date, stop_date, resolution):
            # no time works, this event cannot be scheduled here
            if event.check(start_time) < 1:
                continue

            # fits within the event constraints
            # score event against sched
            ev = ScheduledEvent(start_time, start_time + event.duration, event.name, event.priority)
            if self.conflicts(ev) > 0:
                continue

            # toss that in schedules
            sch = self.copy()
            sch.events.append(ev)
            schedulesAndScores.append((1, sch))

        return schedulesAndScores

    def _scheduleEvents(self, events: List[Event], start_time : datetime, duration : timedelta) -> Optional['Schedule']:
        if not events:
            return self
        event = events.pop()  # list of events which have not been scheduled
        # TODO: consider randomizing schedule choice order
        for score, sched in self.makeSchedules(event, start_time, start_time + duration, TIME_INC):
            next_sched = sched._scheduleEvents(events, start_time, duration)
            if next_sched:
                return next_sched
        # no schedule was found
        events.append(event)
        # if any(x.priority == 0 for x in events):  # any unscheduled event has a priority of 0
        #     return None  # you fail
        # return self  # having unscheduled events is ok if priority > 0 and we exhausted all other options
        return None

    def scheduleEvents(self, events: List[Event], start_time : datetime, duration : timedelta) -> Optional['Schedule']:
        events.sort(key=lambda x: x.priority)  # lower priority gets scheduled first
        return self._scheduleEvents(events, start_time, duration)
