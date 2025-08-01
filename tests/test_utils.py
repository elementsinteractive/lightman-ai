import datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time
from lightman_ai.exceptions import MultipleDateSourcesError
from lightman_ai.utils import get_start_date


class FakeSettings:
    TIME_ZONE = "UTC"


class TestUtils:
    @pytest.mark.parametrize(
        ("today", "yesterday", "start_date", "expected"),
        [
            (True, False, None, datetime.datetime(2025, 7, 30, 0, 0, tzinfo=ZoneInfo("UTC"))),
            (False, True, None, datetime.datetime(2025, 7, 29, 0, 0, tzinfo=ZoneInfo("UTC"))),
            (False, False, datetime.date(2025, 1, 1), datetime.datetime(2025, 1, 1, 0, 0, tzinfo=ZoneInfo("UTC"))),
            (False, False, None, None),
        ],
    )
    @freeze_time("2025-07-30")
    def test_get_start_date(
        self, today: bool, yesterday: bool, start_date: datetime.date, expected: datetime.datetime
    ) -> None:
        settings = FakeSettings()
        start_date_time = get_start_date(settings, yesterday, today, start_date)  # type: ignore[arg-type]
        assert start_date_time == expected

    @pytest.mark.parametrize(
        ("today", "yesterday", "start_date"),
        [
            (True, True, None),
            (True, False, datetime.date(2025, 1, 1)),
            (False, True, datetime.date(2025, 1, 1)),
        ],
    )
    def test_get_start_date_mutually_exclusive_fields(
        self,
        today: bool,
        yesterday: bool,
        start_date: datetime.date,
    ) -> None:
        with pytest.raises(
            MultipleDateSourcesError,
            match="--today, --yesterday and --start-date are mutually exclusive. Set one at a time.",
        ):
            get_start_date(Mock(), yesterday, today, start_date)
