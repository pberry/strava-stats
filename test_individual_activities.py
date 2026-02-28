"""Tests for querying individual activities."""
import json
import os
import tempfile
from database import save_activities, get_individual_activities


def _sample_activities():
    return [
        {
            'id': 1,
            'name': 'Morning Run',
            'type': 'Run',
            'start_date': '2026-02-17T06:30:00Z',
            'distance': 5000.0,
            'moving_time': 1800,
            'total_elevation_gain': 50.0,
        },
        {
            'id': 2,
            'name': 'Afternoon Hike',
            'type': 'Hike',
            'start_date': '2026-02-18T14:00:00Z',
            'distance': 8000.0,
            'moving_time': 7200,
            'total_elevation_gain': 300.0,
        },
        {
            'id': 3,
            'name': 'Evening Walk',
            'type': 'Walk',
            'start_date': '2026-02-20T18:00:00Z',
            'distance': 3000.0,
            'moving_time': 2400,
            'total_elevation_gain': 10.0,
        },
    ]


def _setup_db(activities=None):
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    save_activities(activities or _sample_activities(), db_path=db_path)
    return db_path


def test_returns_activity_details_with_name_from_json():
    """Returns list of dicts with activity details including name from json_payload."""
    db_path = _setup_db()

    try:
        results = get_individual_activities(db_path=db_path)

        assert len(results) == 3
        assert results[0]['name'] == 'Morning Run'
        assert results[0]['activity_id'] == 1
        assert results[0]['date'] == '2026-02-17T06:30:00Z'
        assert results[0]['type'] == 'Run'
        assert results[0]['distance'] == 5000.0
        assert results[0]['time'] == 1800
        assert results[0]['elevation'] == 50.0
    finally:
        os.unlink(db_path)


def test_filters_by_date_range():
    """Filters activities by start_date and end_date."""
    db_path = _setup_db()

    try:
        results = get_individual_activities(
            start_date='2026-02-17',
            end_date='2026-02-18',
            db_path=db_path
        )

        assert len(results) == 2
        assert results[0]['name'] == 'Morning Run'
        assert results[1]['name'] == 'Afternoon Hike'
    finally:
        os.unlink(db_path)


def test_filters_by_activity_type():
    """Filters activities by type."""
    db_path = _setup_db()

    try:
        results = get_individual_activities(
            activity_type='Hike',
            db_path=db_path
        )

        assert len(results) == 1
        assert results[0]['name'] == 'Afternoon Hike'
    finally:
        os.unlink(db_path)


def test_returns_empty_list_when_no_match():
    """Returns empty list when no activities match filters."""
    db_path = _setup_db()

    try:
        results = get_individual_activities(
            start_date='2026-03-01',
            end_date='2026-03-07',
            db_path=db_path
        )

        assert results == []
    finally:
        os.unlink(db_path)


def test_orders_by_date_ascending():
    """Results ordered by date ascending."""
    db_path = _setup_db()

    try:
        results = get_individual_activities(db_path=db_path)

        dates = [r['date'] for r in results]
        assert dates == sorted(dates)
    finally:
        os.unlink(db_path)
