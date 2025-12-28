"""Tests for sync integration."""
import os
import tempfile
from unittest.mock import patch, Mock
from sync import sync_activities
from database import get_last_sync, get_activities


def test_sync_activities_fetches_and_stores_new_activities():
    """Fetches activities since last sync and updates timestamp."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        # Mock Strava API to return 2 activities
        mock_activities = [
            {
                'id': 1,
                'name': 'Run 1',
                'type': 'Run',
                'start_date': '2025-01-15T06:00:00Z',
                'distance': 5000.0,
                'moving_time': 1800,
                'total_elevation_gain': 50.0
            },
            {
                'id': 2,
                'name': 'Run 2',
                'type': 'Run',
                'start_date': '2025-01-16T06:00:00Z',
                'distance': 6000.0,
                'moving_time': 2100,
                'total_elevation_gain': 60.0
            }
        ]

        with patch('sync.fetch_activities', return_value=mock_activities):
            with patch('sync.time.time', return_value=1705420800):  # Mock current time
                sync_activities(access_token='test_token', db_path=db_path)

        # Verify activities were saved
        saved = get_activities(db_path=db_path)
        assert len(saved) == 2
        assert saved[0]['activity_id'] == 1
        assert saved[1]['activity_id'] == 2

        # Verify last sync timestamp was updated
        last_sync = get_last_sync(db_path=db_path)
        assert last_sync == 1705420800

    finally:
        os.unlink(db_path)


def test_sync_activities_uses_last_sync_as_after_parameter():
    """Uses last sync timestamp as 'after' parameter for incremental sync."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        # Set existing last sync timestamp
        from database import update_last_sync
        update_last_sync(1705334400, db_path=db_path)  # 2024-01-15 12:00:00

        mock_activities = [
            {
                'id': 3,
                'name': 'Run 3',
                'type': 'Run',
                'start_date': '2025-01-17T06:00:00Z',
                'distance': 7000.0,
                'moving_time': 2400,
                'total_elevation_gain': 70.0
            }
        ]

        with patch('sync.fetch_activities', return_value=mock_activities) as mock_fetch:
            with patch('sync.time.time', return_value=1705507200):
                sync_activities(access_token='test_token', db_path=db_path)

            # Verify fetch_activities was called with after=last_sync_timestamp
            mock_fetch.assert_called_once_with(
                access_token='test_token',
                after=1705334400
            )

    finally:
        os.unlink(db_path)
