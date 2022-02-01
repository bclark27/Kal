from datetime import datetime, timedelta
from typing import List, Iterator, Tuple


def generate_times(start_date: datetime, stop_date: datetime, resolution: timedelta) -> Iterator[datetime]:
    if start_date > stop_date:
        return

    time_inc = start_date
    while time_inc < stop_date:
        yield time_inc
        time_inc += resolution
