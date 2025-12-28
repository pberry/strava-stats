#!/usr/bin/env python3
"""Sync activities from Strava API to local database."""
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from strava_api import fetch_activities
from database import save_activities, get_last_sync, update_last_sync


def sync_activities(access_token, db_path='strava.db'):
    """Fetch activities since last sync and save to database."""
    last_sync = get_last_sync(db_path=db_path)

    activities = fetch_activities(access_token=access_token, after=last_sync)

    if activities:
        save_activities(activities, db_path=db_path)

    current_time = int(time.time())
    update_last_sync(current_time, db_path=db_path)

    return len(activities)


def main():
    """Main entry point for sync command."""
    load_dotenv()

    access_token = os.getenv('STRAVA_ACCESS_TOKEN')
    if not access_token:
        print("✗ Error: STRAVA_ACCESS_TOKEN not found in .env", file=sys.stderr)
        return 1

    try:
        last_sync = get_last_sync()
        if last_sync:
            last_sync_dt = datetime.fromtimestamp(last_sync)
            print(f"Syncing activities since {last_sync_dt.strftime('%Y-%m-%d %H:%M:%S')}...")
        else:
            print("First sync - fetching all activities...")

        count = sync_activities(access_token=access_token)

        if count > 0:
            print(f"✓ Synced {count} activities")
        else:
            print("✓ No new activities")

        return 0

    except RuntimeError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
