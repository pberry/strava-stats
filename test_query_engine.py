"""Tests for activity query engine."""
import os
import tempfile
from database import save_activities
from query_engine import query_activities


def test_query_activities_filters_by_activity_type():
    """Filters activities by type (Hike, Run, Walk, etc)."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 1,
                'name': 'Morning Run',
                'type': 'Run',
                'start_date': '2025-01-15T06:00:00Z',
                'distance': 5000.0,
                'moving_time': 1800,
                'total_elevation_gain': 50.0
            },
            {
                'id': 2,
                'name': 'Afternoon Hike',
                'type': 'Hike',
                'start_date': '2025-01-15T14:00:00Z',
                'distance': 8000.0,
                'moving_time': 7200,
                'total_elevation_gain': 300.0
            },
            {
                'id': 3,
                'name': 'Evening Walk',
                'type': 'Walk',
                'start_date': '2025-01-15T18:00:00Z',
                'distance': 3000.0,
                'moving_time': 1800,
                'total_elevation_gain': 10.0
            }
        ]

        save_activities(activities, db_path=db_path)

        # Query only hikes
        result = query_activities(activity_type='Hike', db_path=db_path)

        assert result['count'] == 1
        assert result['total_distance'] == 8000.0
        assert result['total_time'] == 7200
        assert result['total_elevation'] == 300.0

    finally:
        os.unlink(db_path)


def test_query_activities_filters_by_date_range():
    """Filters activities by date range."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 1,
                'name': 'January Hike',
                'type': 'Hike',
                'start_date': '2025-01-15T06:00:00Z',
                'distance': 5000.0,
                'moving_time': 1800,
                'total_elevation_gain': 100.0
            },
            {
                'id': 2,
                'name': 'February Hike',
                'type': 'Hike',
                'start_date': '2025-02-15T06:00:00Z',
                'distance': 6000.0,
                'moving_time': 2100,
                'total_elevation_gain': 150.0
            },
            {
                'id': 3,
                'name': 'March Hike',
                'type': 'Hike',
                'start_date': '2025-03-15T06:00:00Z',
                'distance': 7000.0,
                'moving_time': 2400,
                'total_elevation_gain': 200.0
            }
        ]

        save_activities(activities, db_path=db_path)

        # Query only February
        result = query_activities(
            start_date='2025-02-01',
            end_date='2025-02-28',
            db_path=db_path
        )

        assert result['count'] == 1
        assert result['total_distance'] == 6000.0

    finally:
        os.unlink(db_path)
