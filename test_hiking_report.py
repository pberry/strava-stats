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
