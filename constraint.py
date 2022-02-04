from abc import ABC
from datetime import datetime, timedelta, date, time
from enum import Enum, auto
from typing import List

from dataclasses import dataclass
from dateutil.relativedelta import relativedelta


def check_for_multiple_days():
    pass


class Constraint(ABC):
    def _check(self, start: datetime, end: datetime) -> float:
        """
        :return: number of seconds available
        """
        raise NotImplementedError

    def check(self, start: datetime, end: datetime):
        """
        Check a given timespan is within a constraint. This assumes start < end.

        :return: percent availability from [0, 1]
        """
        if start.date() >= end.date():
            if start == end:
                return 1.0
            else:
                return self._check(start, end) / (end - start).total_seconds()

        times = [(start, datetime.combine(start, time.max))]

        start_date = start
        # get all the discrete days that are necessary for this timespan
        while start_date < end:
            start_date += timedelta(days=1)
            if start_date.date() == end.date():
                times.append((datetime.combine(start_date, time.min), end))
            else:
                times.append((datetime.combine(start_date, time.min), datetime.combine(start_date, time.max)))

        total_seconds_available = sum(self._check(st, et) for st, et in times)
        return total_seconds_available / (end - start).total_seconds()


# the chad
class NullConstraint(Constraint):
    def _check(self, start: datetime, end: datetime) -> float:
        return (end - start).total_seconds()


@dataclass()
class TimeOfDayConstraint(Constraint):
    start: time
    end: time

    def _check(self, start: datetime, end: datetime) -> float:
        s = min(end.time(), self.end)
        e = max(start.time(), self.start)
        diff = timedelta(hours=s.hour, minutes=s.minute, seconds=s.second) - timedelta(hours=e.hour, minutes=e.minute, seconds=e.second)
        return max(diff.total_seconds(), 0)


@dataclass()
class DateConstraint(Constraint):
    start: datetime
    end: datetime

    def _check(self, start: datetime, end: datetime) -> float:
        """
        Check a given timespan is within a constraint. This assumes start < end.

        :return: True if valid
        """
        e = min(end, self.end)
        s = max(start, self.start)
        diff = e - s
        return max(diff.total_seconds(), 0)


@dataclass()
class DayOfWeekConstraint(Constraint):
    dow: int  # 0-6

    def _check(self, start: datetime, end: datetime) -> float:
        if start.weekday() == self.dow:
            return (end - start).total_seconds()
        else:
            return 0.0


@dataclass()
class DayOfMonthConstraint(Constraint):
    dom: int  # 1-31

    def _check(self, start: datetime, end: datetime) -> float:
        if start.day == self.dom:
            return (end - start).total_seconds()
        else:
            return 0.0


@dataclass()
class WeekOfMonthConstraint(Constraint):
    wom: int  # 1-5

    def _check(self, start: datetime, end: datetime) -> float:
        if (start.day - 1) // 7 + 1 == self.wom:
            return (end - start).total_seconds()
        else:
            return 0.0


class RepetitiveType(Enum):
    DAILY = auto()  # nat
    WEEKLY = auto()  # nat
    MONTHLY = auto()  # nat
    YEARLY = auto()  # nat


@dataclass()
class ConstraintUnion(Constraint):
    constraints: List['Constraint']

    def _check(self, start: datetime, end: datetime) -> float:
        total_time = 0.0
        max_time = (end - start).total_seconds()
        for con in self.constraints:
            total_time = max(total_time, con._check(start, end))
            if total_time >= max_time:
                return max_time

        return total_time


@dataclass()
class ConstraintIntersect(Constraint):
    constraints: List['Constraint']

    def _check(self, start: datetime, end: datetime) -> float:
        total_time = (end - start).total_seconds()
        for con in self.constraints:
            total_time = min(total_time, con._check(start, end))
            if total_time <= 0.0:
                return 0.0

        return total_time


@dataclass()
class RepetitiveConstraint(Constraint):
    constraint: Constraint
    repType: RepetitiveType
    repTime: int
    basisTime: date

    def _check(self, start: datetime, end: datetime):
        day = start.date()

        if self.repType == RepetitiveType.DAILY:
            diff_days = day - self.basisTime
            if diff_days.days % self.repTime != 0:
                return 0.0
        elif self.repType == RepetitiveType.WEEKLY:
            diff_days = day - self.basisTime
            if (diff_days.days // 7) % self.repTime != 0:
                return 0.0
        elif self.repType == RepetitiveType.MONTHLY:
            diff_months = relativedelta(day.replace(day=1), self.basisTime.replace(day=1)).months
            if diff_months % self.repTime != 0:
                return 0.0
        elif self.repType == RepetitiveType.YEARLY:
            diff_years = day.year - self.basisTime.year
            if diff_years % self.repTime != 0:
                return 0.0

        return self.constraint._check(start, end)


# COMMON CONSTRAINT GENERATORS

def gen_multi_day_constraint(days: list[int]):
    """
    Generate a constraint which restricts a date to any of the days given.
    0 = mon, 1 = tues, 2 = wed, 3 = thur, 4 = fri, 5 = sat, 6 = sun

    :param days: sequence of days to allow
    :return: constraint of day1 OR day2 or day3 OR ...
    """
    return ConstraintUnion([DayOfWeekConstraint(day) for day in days])
