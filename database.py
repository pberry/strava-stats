"""SQLite database for storing Strava activities."""
import json
import sqlite3


def _init_database(db_path):
    """Create database and schema if they don't exist."""
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    activity_id INTEGER PRIMARY KEY,
                    date TEXT,
                    type TEXT,
                    distance REAL,
                    time INTEGER,
                    elevation REAL,
                    json_payload TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sync_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to initialize database at {db_path}: {e}")


def _extract_activity_fields(activity):
    """Extract required fields from activity dict."""
    required = ['id', 'start_date', 'type', 'distance', 'moving_time', 'total_elevation_gain']
    for field in required:
        if field not in activity:
            raise RuntimeError(
                f"Activity missing required field '{field}'. "
                f"Available fields: {list(activity.keys())}"
            )

    return (
        activity['id'],
        activity['start_date'],
        activity['type'],
        activity['distance'],
        activity['moving_time'],
        activity['total_elevation_gain'],
        json.dumps(activity)
    )


def save_activities(activities, db_path='strava.db'):
    """Save activities to database (upsert by activity_id)."""
    _init_database(db_path)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            for activity in activities:
                fields = _extract_activity_fields(activity)
                cursor.execute('''
                    INSERT OR REPLACE INTO activities
                    (activity_id, date, type, distance, time, elevation, json_payload)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', fields)
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to save activities to database: {e}")


def get_activities(db_path='strava.db', **filters):
    """Query activities from database."""
    _init_database(db_path)

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM activities')
            rows = cursor.fetchall()

            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to query activities from database: {e}")


def get_last_sync(db_path='strava.db'):
    """Get timestamp of last successful sync."""
    _init_database(db_path)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT value FROM sync_metadata WHERE key = 'last_sync'"
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return int(row[0])
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to get last sync timestamp: {e}")


def update_last_sync(timestamp, db_path='strava.db'):
    """Update timestamp of last successful sync."""
    _init_database(db_path)

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO sync_metadata (key, value) VALUES ('last_sync', ?)",
                (str(timestamp),)
            )
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to update last sync timestamp: {e}")
