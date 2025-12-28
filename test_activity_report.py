"""Tests for generic activity miles report."""
import os
import tempfile
from database import save_activities
from activity_report import calculate_activity_miles


def test_calculate_activity_miles_works_for_runs():
    """Calculates total miles for runs with monthly breakdown."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 1,
                'name': 'Morning Run',
                'type': 'Run',
                'start_date': '2025-01-10T06:00:00Z',
                'distance': 8046.72,  # 5 miles
                'moving_time': 2400,
                'total_elevation_gain': 50.0
            },
            {
                'id': 2,
                'name': 'Evening Run',
                'type': 'Run',
                'start_date': '2025-01-20T18:00:00Z',
                'distance': 4828.03,  # 3 miles
                'moving_time': 1800,
                'total_elevation_gain': 30.0
            },
            {
                'id': 3,
                'name': 'Weekend Hike',
                'type': 'Hike',
                'start_date': '2025-01-15T10:00:00Z',
                'distance': 16093.4,  # 10 miles
                'moving_time': 14400,
                'total_elevation_gain': 500.0
            }
        ]

        save_activities(activities, db_path=db_path)

        result = calculate_activity_miles(year=2025, activity_type='Run', db_path=db_path)

        # Should be 8 miles total (5 + 3, excluding the hike)
        assert result['total_miles'] == 8.0
        assert result['activity_count'] == 2
        assert 'monthly_breakdown' in result
        assert len(result['monthly_breakdown']) == 1
        assert result['monthly_breakdown'][0]['month'] == 'January'
        assert result['monthly_breakdown'][0]['miles'] == 8.0

    finally:
        os.unlink(db_path)
