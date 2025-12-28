"""Tests for SQLite database storage."""
import os
import sqlite3
import tempfile
from database import save_activities, get_activities


def test_save_activities_stores_extracted_fields_and_json():
    """Saves activities with extracted fields and full JSON payload."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        activities = [
            {
                'id': 123,
                'name': 'Morning Run',
                'type': 'Run',
                'start_date': '2025-01-15T06:30:00Z',
                'distance': 5000.0,
                'moving_time': 1800,
                'total_elevation_gain': 50.0,
                'sport_type': 'Run'
            },
            {
                'id': 456,
                'name': 'Evening Hike',
                'type': 'Hike',
                'start_date': '2025-01-15T18:00:00Z',
                'distance': 8000.0,
                'moving_time': 7200,
                'total_elevation_gain': 300.0,
                'sport_type': 'Hike'
            }
        ]

        save_activities(activities, db_path=db_path)

        # Verify activities were saved with extracted fields
        saved = get_activities(db_path=db_path)

        assert len(saved) == 2
        assert saved[0]['activity_id'] == 123
        assert saved[0]['type'] == 'Run'
        assert saved[0]['distance'] == 5000.0
        assert saved[1]['activity_id'] == 456
        assert saved[1]['elevation'] == 300.0

    finally:
        os.unlink(db_path)
