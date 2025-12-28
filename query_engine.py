"""Query engine for filtering and aggregating activities."""
import sqlite3
from database import _init_database


def query_activities(activity_type=None, start_date=None, end_date=None, db_path='strava.db'):
    """Query activities with filters and return aggregated metrics."""
    _init_database(db_path)

    query = "SELECT COUNT(*), SUM(distance), SUM(time), SUM(elevation) FROM activities WHERE 1=1"
    params = []

    if activity_type:
        query += " AND type = ?"
        params.append(activity_type)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()

            count, total_distance, total_time, total_elevation = row

            return {
                'count': count or 0,
                'total_distance': total_distance or 0.0,
                'total_time': total_time or 0,
                'total_elevation': total_elevation or 0.0
            }
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to query activities: {e}")
