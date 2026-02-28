#!/usr/bin/env python3
"""Weekly post CLI orchestrator."""
import argparse
import os
import sys
import time
import sqlite3
from datetime import datetime, timedelta, timezone
from token_manager import get_access_token
from sync import sync_activities
from database import get_individual_activities, _init_database
from weekly_report import format_weekly_report
from wordpress import create_post, load_wp_credentials


def get_week_boundaries(today):
    """Return (start_date, end_date) strings for the Mon-Sun week containing today."""
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return (monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))


def _get_last_post_time(db_path='strava.db'):
    """Get timestamp of last successful post from sync_metadata."""
    _init_database(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT value FROM sync_metadata WHERE key = 'last_post_time'"
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return int(row[0])
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to get last post time: {e}")


def _update_last_post_time(timestamp, db_path='strava.db'):
    """Update timestamp of last successful post in sync_metadata."""
    _init_database(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO sync_metadata (key, value) VALUES ('last_post_time', ?)",
                (str(timestamp),)
            )
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to update last post time: {e}")


def main(env_file='.env', db_path='strava.db', dry_run=False):
    """Main entry point for weekly post."""
    try:
        access_token = get_access_token(env_file=env_file)

        sync_activities(access_token=access_token, db_path=db_path)

        now = int(time.time())
        today = datetime.fromtimestamp(now, tz=timezone.utc).date()
        start_date, end_date = get_week_boundaries(today)

        activities = get_individual_activities(
            start_date=start_date,
            end_date=end_date,
            db_path=db_path,
        )

        if not activities:
            print("No activities found for this period. Skipping post.")
            return 0

        report = format_weekly_report(activities, start_date=start_date, end_date=end_date)

        title = f"Weekly Activities: {_format_title_date_range(start_date, end_date)}"

        if dry_run:
            print(f"[dry-run] Title: {title}")
            print(report)
            return 0

        wp_creds = load_wp_credentials(env_file=env_file)

        result = create_post(
            wp_url=wp_creds['wp_url'],
            username=wp_creds['username'],
            app_password=wp_creds['app_password'],
            title=title,
            content=report,
        )

        _update_last_post_time(now, db_path=db_path)

        print(f"Posted: {result['link']}")
        return 0

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _format_title_date_range(start_date, end_date):
    """Format date range for post title."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if start.month == end.month:
        return f"{start.strftime('%b')} {start.day}-{end.day}, {end.year}"
    return f"{start.strftime('%b')} {start.day} - {end.strftime('%b')} {end.day}, {end.year}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Post weekly activity report to WordPress.')
    parser.add_argument('--dry-run', action='store_true', help='Print report without posting.')
    args = parser.parse_args()
    sys.exit(main(dry_run=args.dry_run))
