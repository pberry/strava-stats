"""Tests for sync timestamp tracking."""
import os
import tempfile
from database import get_last_sync, update_last_sync


def test_get_last_sync_returns_none_when_never_synced():
    """Returns None when no sync has been performed yet."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        last_sync = get_last_sync(db_path=db_path)
        assert last_sync is None
    finally:
        os.unlink(db_path)


def test_update_and_get_last_sync_timestamp():
    """Stores and retrieves last sync timestamp."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        # First sync has no timestamp
        assert get_last_sync(db_path=db_path) is None

        # Update with a timestamp
        timestamp = 1705334400  # 2024-01-15 12:00:00 UTC
        update_last_sync(timestamp, db_path=db_path)

        # Retrieve it
        last_sync = get_last_sync(db_path=db_path)
        assert last_sync == timestamp

        # Update again with newer timestamp
        new_timestamp = 1705420800  # 2024-01-16 12:00:00 UTC
        update_last_sync(new_timestamp, db_path=db_path)

        # Should return the newer one
        last_sync = get_last_sync(db_path=db_path)
        assert last_sync == new_timestamp

    finally:
        os.unlink(db_path)
