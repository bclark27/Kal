from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import List, Generator
from constraint import *
from schedule import Schedule
from event import Event
from dataclasses import dataclass
import util
from schedule_parser import lexer

with open("schedule.txt") as f:
    sched_data = f.read()

lexer.input(sched_data)
while True:
     tok = lexer.token()
     if not tok:
         break  # No more input
     print(tok)

exit()

sch = Schedule([])
events = [
    Event.create_basic("HW1", 7, DayOfWeekConstraint(3), priority=2),
    Event.create_basic("HW2", 5, DayOfWeekConstraint(3), priority=2),
    Event.create_basic("HW3", 2, DayOfWeekConstraint(3), priority=3),
    Event.create_basic("HW4", 1, DayOfWeekConstraint(0), priority=4),
    Event.create_basic("HW5", 5, DayOfWeekConstraint(1), priority=2),
    Event.create_basic("HW6", 10, DateConstraint(parse("12/03"), parse("12/04")), priority=1),
    Event.create_basic("CLASS", 5, RepetitiveConstraint(ConstraintIntersect([DayOfWeekConstraint(2), TimeOfDayConstraint(time(12), time(17))]), RepetitiveType.WEEKLY, 1, date(2021, 10, 27))),
    Event.create_basic("SLEEP", 8, RepetitiveConstraint(TimeOfDayConstraint(time.min, time(8)), RepetitiveType.DAILY, 1, date(2021, 10, 27)))
]
good = sch.scheduleEvents(events=events,
                          start_time=datetime.now().replace(minute=0, second=0, microsecond=0),
                          duration=timedelta(days=7))
print(good)
