from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from lightman_ai.exceptions import MultipleDateSourcesError


def get_start_date(time_zone: str, yesterday: bool, today: bool, start_date: date | None) -> datetime | None:
    mutually_exclusive_date_fields = [x for x in [start_date, today, yesterday] if x]

    if len(mutually_exclusive_date_fields) > 1:
        raise MultipleDateSourcesError(
            "--today, --yesterday and --start-date are mutually exclusive. Set one at a time."
        )

    if today:
        now = datetime.now(ZoneInfo(time_zone))
        return datetime.combine(now, time(0, 0), tzinfo=ZoneInfo(time_zone))
    elif yesterday:
        yesterday_date = datetime.now(ZoneInfo(time_zone)) - timedelta(days=1)
        return datetime.combine(yesterday_date, time(0, 0), tzinfo=ZoneInfo(time_zone))
    elif isinstance(start_date, date):
        return datetime.combine(start_date, time(0, 0), tzinfo=ZoneInfo(time_zone))
    else:
        return None
