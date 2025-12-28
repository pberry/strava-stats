"""Hiking miles report generator."""
from activity_report import calculate_activity_miles


def calculate_hiking_miles(year, db_path='strava.db'):
    """Calculate total hiking miles for a given year."""
    return calculate_activity_miles(year, 'Hike', db_path)
