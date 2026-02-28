"""Tests for weekly report formatter."""
from weekly_report import format_weekly_report


def _sample_activities():
    return [
        {
            'activity_id': 1,
            'name': 'Morning Run',
            'date': '2026-02-17T06:30:00Z',
            'type': 'Run',
            'distance': 8046.7,
            'time': 2700,
            'elevation': 30.48,
        },
        {
            'activity_id': 2,
            'name': 'Trail Hike',
            'date': '2026-02-18T14:00:00Z',
            'type': 'Hike',
            'distance': 16093.4,
            'time': 10800,
            'elevation': 304.8,
        },
        {
            'activity_id': 3,
            'name': 'Evening Run',
            'date': '2026-02-20T18:00:00Z',
            'type': 'Run',
            'distance': 4828.0,
            'time': 1800,
            'elevation': 15.24,
        },
    ]


def test_title_includes_date_range():
    """Title includes date range: 'Activities: Feb 17-23, 2026'."""
    report = format_weekly_report(
        _sample_activities(),
        start_date='2026-02-17',
        end_date='2026-02-23',
    )

    assert "Activities: Feb 17-23, 2026" in report


def test_title_date_range_spanning_months():
    """Date range spanning months: 'Activities: Jan 28 - Feb 3, 2026'."""
    report = format_weekly_report(
        _sample_activities(),
        start_date='2026-01-28',
        end_date='2026-02-03',
    )

    assert "Activities: Jan 28 - Feb 3, 2026" in report


def test_activity_shows_details():
    """Each activity shows day-of-week, name, type, distance, time, elevation."""
    report = format_weekly_report(
        _sample_activities(),
        start_date='2026-02-17',
        end_date='2026-02-23',
    )

    assert "Morning Run" in report
    assert "5.00 mi" in report
    assert "45m" in report
    assert "100 ft" in report


def test_activity_name_links_to_strava():
    """Each activity name is a markdown link to its Strava activity page."""
    report = format_weekly_report(
        _sample_activities(),
        start_date='2026-02-17',
        end_date='2026-02-23',
    )

    assert "[Morning Run](https://www.strava.com/activities/1)" in report
    assert "[Trail Hike](https://www.strava.com/activities/2)" in report
    assert "[Evening Run](https://www.strava.com/activities/3)" in report


def test_converts_meters_to_miles():
    """Converts distance from meters to miles (÷ 1609.34)."""
    activities = [{
        'activity_id': 1,
        'name': 'Test Run',
        'date': '2026-02-17T06:00:00Z',
        'type': 'Run',
        'distance': 1609.34,
        'time': 600,
        'elevation': 0.0,
    }]

    report = format_weekly_report(activities, start_date='2026-02-17', end_date='2026-02-23')
    assert "1.00 mi" in report


def test_converts_meters_to_feet():
    """Converts elevation from meters to feet (× 3.281)."""
    activities = [{
        'activity_id': 1,
        'name': 'Test Hike',
        'date': '2026-02-17T06:00:00Z',
        'type': 'Hike',
        'distance': 5000.0,
        'time': 3600,
        'elevation': 304.8,
    }]

    report = format_weekly_report(activities, start_date='2026-02-17', end_date='2026-02-23')
    assert "1,000 ft" in report


def test_formats_time_hours_and_minutes():
    """Formats time: '1h 30m' for 5400s."""
    activities = [{
        'activity_id': 1,
        'name': 'Long Run',
        'date': '2026-02-17T06:00:00Z',
        'type': 'Run',
        'distance': 5000.0,
        'time': 5400,
        'elevation': 0.0,
    }]

    report = format_weekly_report(activities, start_date='2026-02-17', end_date='2026-02-23')
    assert "1h 30m" in report


def test_formats_time_minutes_only():
    """Formats time: '30m' for 1800s (no hours shown)."""
    activities = [{
        'activity_id': 1,
        'name': 'Short Run',
        'date': '2026-02-17T06:00:00Z',
        'type': 'Run',
        'distance': 3000.0,
        'time': 1800,
        'elevation': 0.0,
    }]

    report = format_weekly_report(activities, start_date='2026-02-17', end_date='2026-02-23')
    assert "30m" in report
    assert "0h" not in report


def test_summary_with_total_and_type_counts():
    """Summary groups by type: '2 Runs, 1 Hike'."""
    report = format_weekly_report(
        _sample_activities(),
        start_date='2026-02-17',
        end_date='2026-02-23',
    )

    assert "2 Runs" in report
    assert "1 Hike" in report


def test_empty_activities():
    """Empty activities → 'No activities this week.'."""
    report = format_weekly_report(
        [],
        start_date='2026-02-17',
        end_date='2026-02-23',
    )

    assert "No activities this week." in report
