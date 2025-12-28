"""Tests for hiking miles report."""
import os
import tempfile
from database import save_activities
from hiking_report import calculate_hiking_miles


def test_calculate_hiking_miles_converts_meters_to_miles():
    """Calculates total hiking miles for a year, converting from meters."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 1,
                'name': 'Hike 1',
                'type': 'Hike',
                'start_date': '2025-01-15T06:00:00Z',
                'distance': 1609.34,  # 1 mile in meters
                'moving_time': 1800,
                'total_elevation_gain': 100.0
            },
            {
                'id': 2,
                'name': 'Hike 2',
                'type': 'Hike',
                'start_date': '2025-02-15T06:00:00Z',
                'distance': 3218.68,  # 2 miles in meters
                'moving_time': 3600,
                'total_elevation_gain': 200.0
            },
            {
                'id': 3,
                'name': 'Run (not a hike)',
                'type': 'Run',
                'start_date': '2025-03-15T06:00:00Z',
                'distance': 5000.0,
                'moving_time': 2000,
                'total_elevation_gain': 50.0
            }
        ]

        save_activities(activities, db_path=db_path)

        # Calculate hiking miles for 2025
        result = calculate_hiking_miles(year=2025, db_path=db_path)

        # Should be 3 miles total (1 + 2, excluding the run)
        assert result['total_miles'] == 3.0
        assert result['activity_count'] == 2

    finally:
        os.unlink(db_path)


def test_calculate_hiking_miles_includes_monthly_breakdown():
    """Includes monthly breakdown with miles and count per month."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 1,
                'name': 'January Hike 1',
                'type': 'Hike',
                'start_date': '2025-01-10T06:00:00Z',
                'distance': 1609.34,  # 1 mile
                'moving_time': 1800,
                'total_elevation_gain': 100.0
            },
            {
                'id': 2,
                'name': 'January Hike 2',
                'type': 'Hike',
                'start_date': '2025-01-20T06:00:00Z',
                'distance': 3218.68,  # 2 miles
                'moving_time': 3600,
                'total_elevation_gain': 200.0
            },
            {
                'id': 3,
                'name': 'February Hike',
                'type': 'Hike',
                'start_date': '2025-02-15T06:00:00Z',
                'distance': 4828.02,  # 3 miles
                'moving_time': 5400,
                'total_elevation_gain': 300.0
            }
        ]

        save_activities(activities, db_path=db_path)

        result = calculate_hiking_miles(year=2025, db_path=db_path)

        assert 'monthly_breakdown' in result
        assert len(result['monthly_breakdown']) == 2

        # January: 3 miles, 2 hikes
        january = result['monthly_breakdown'][0]
        assert january['month'] == 'January'
        assert january['miles'] == 3.0
        assert january['count'] == 2

        # February: 3 miles, 1 hike
        february = result['monthly_breakdown'][1]
        assert february['month'] == 'February'
        assert february['miles'] == 3.0
        assert february['count'] == 1

    finally:
        os.unlink(db_path)
