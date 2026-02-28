"""Weekly report formatter for Strava activities."""
from collections import Counter
from datetime import datetime

METERS_PER_MILE = 1609.34
METERS_TO_FEET = 3.281

ACTIVITY_PLURALS = {
    'Run': 'Runs',
    'Hike': 'Hikes',
    'Walk': 'Walks',
    'Ride': 'Rides',
}


def format_weekly_report(activities, start_date, end_date):
    """Format a weekly report of individual activities."""
    title = _format_title(start_date, end_date)
    lines = [f"# {title}", ""]

    if not activities:
        lines.append("No activities this week.")
        return "\n".join(lines)

    for activity in activities:
        lines.append(_format_activity_line(activity))

    lines.append("")
    lines.append(_format_summary(activities))

    return "\n".join(lines)


def _format_title(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    if start.month == end.month:
        return f"Activities: {start.strftime('%b')} {start.day}-{end.day}, {end.year}"

    return f"Activities: {start.strftime('%b')} {start.day} - {end.strftime('%b')} {end.day}, {end.year}"


def _format_activity_line(activity):
    date = datetime.strptime(activity['date'][:10], '%Y-%m-%d')
    day_str = date.strftime('%a %m/%d')
    name = activity['name']
    distance = activity['distance'] / METERS_PER_MILE
    time_str = _format_duration(activity['time'])
    elevation = activity['elevation'] * METERS_TO_FEET

    return f"- **{day_str}**: {name} — {distance:.2f} mi, {time_str}, {elevation:,.0f} ft"


def _format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def _format_summary(activities):
    total_distance = sum(a['distance'] for a in activities) / METERS_PER_MILE
    total_time = sum(a['time'] for a in activities)
    type_counts = Counter(a['type'] for a in activities)

    type_parts = []
    for activity_type, count in type_counts.items():
        label = ACTIVITY_PLURALS.get(activity_type, activity_type + 's')
        if count == 1:
            label = activity_type
        type_parts.append(f"{count} {label}")

    summary_line = ", ".join(type_parts)
    return f"**Totals**: {total_distance:.2f} mi, {_format_duration(total_time)} — {summary_line}"
