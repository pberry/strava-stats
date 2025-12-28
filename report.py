#!/usr/bin/env python3
"""Generate combined activity report for Hikes, Runs, and Walks."""
import sys
from activity_report import calculate_activity_miles
from combined_report import format_combined_report


def main():
    """Generate combined activity report."""
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f'✗ Error: Invalid year "{sys.argv[1]}"')
            print('Usage: python report.py [year]')
            return 1
    else:
        import datetime
        year = datetime.datetime.now().year

    print(f'Generating activity report for {year}...\n')

    try:
        # Calculate miles for each activity type
        activities = {}
        for activity_type in ['Hike', 'Run', 'Walk']:
            result = calculate_activity_miles(year, activity_type)
            # Only include if there are activities
            if result['activity_count'] > 0:
                activities[activity_type] = result

        if not activities:
            print(f'No activities found for {year}')
            return 0

        # Format as combined report
        report_data = {
            'year': year,
            'activities': activities
        }
        markdown = format_combined_report(report_data)

        print(markdown)
        return 0

    except Exception as e:
        print(f'✗ Error: {e}')
        return 1


if __name__ == '__main__':
    exit(main())
