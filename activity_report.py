"""Generic activity miles report generator."""
from query_engine import query_activities


METERS_PER_MILE = 1609.34
MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def _last_day_of_month(year, month_num):
    """Calculate last day of month, accounting for leap years."""
    if month_num in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    if month_num in [4, 6, 9, 11]:
        return 30
    # February - check for leap year
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    return 29 if is_leap_year else 28


def _calculate_monthly_breakdown(year, activity_type, db_path):
    """Calculate miles breakdown by month for specific activity type."""
    monthly_breakdown = []
    for month_num in range(1, 13):
        month_start = f'{year}-{month_num:02d}-01'
        last_day = _last_day_of_month(year, month_num)
        month_end = f'{year}-{month_num:02d}-{last_day}'

        month_result = query_activities(
            activity_type=activity_type,
            start_date=month_start,
            end_date=month_end,
            db_path=db_path
        )

        if month_result['count'] > 0:
            month_miles = month_result['total_distance'] / METERS_PER_MILE
            monthly_breakdown.append({
                'month': MONTHS[month_num - 1],
                'miles': round(month_miles, 1),
                'count': month_result['count']
            })

    return monthly_breakdown


def calculate_activity_miles(year, activity_type, db_path='strava.db'):
    """Calculate total miles for any activity type with monthly breakdown."""
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    result = query_activities(
        activity_type=activity_type,
        start_date=start_date,
        end_date=end_date,
        db_path=db_path
    )

    total_miles = result['total_distance'] / METERS_PER_MILE
    monthly_breakdown = _calculate_monthly_breakdown(year, activity_type, db_path)

    return {
        'total_miles': round(total_miles, 1),
        'activity_count': result['count'],
        'monthly_breakdown': monthly_breakdown
    }
