"""Hiking miles report generator."""
from query_engine import query_activities


METERS_PER_MILE = 1609.34


def calculate_hiking_miles(year, db_path='strava.db'):
    """Calculate total hiking miles for a given year."""
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    result = query_activities(
        activity_type='Hike',
        start_date=start_date,
        end_date=end_date,
        db_path=db_path
    )

    total_miles = result['total_distance'] / METERS_PER_MILE

    return {
        'total_miles': round(total_miles, 1),
        'activity_count': result['count']
    }
