"""Combined activity report formatter."""


ACTIVITY_LABELS = {
    'Hike': ('Hikes', 'hikes'),
    'Run': ('Runs', 'runs'),
    'Walk': ('Walks', 'walks')
}


def _format_activity_section(activity_type, activity_data):
    """Format a single activity type section."""
    section_title, activity_label = ACTIVITY_LABELS[activity_type]
    total_miles = activity_data['total_miles']
    activity_count = activity_data['activity_count']

    section = f"## {section_title}\n\n"
    section += f"**Total Miles:** {total_miles}\n"
    section += f"**Total {section_title}:** {activity_count}\n"

    if 'monthly_breakdown' in activity_data and activity_data['monthly_breakdown']:
        section += "\n### Monthly Breakdown\n\n"
        for month_data in activity_data['monthly_breakdown']:
            month = month_data['month']
            miles = month_data['miles']
            count = month_data['count']
            section += f"**{month}:** {miles} miles ({count} {activity_label})\n"

    return section


def format_combined_report(report_data):
    """Format multiple activity types in single markdown report."""
    year = report_data['year']
    activities = report_data['activities']

    output = f"# {year} Activity Report\n\n"

    for activity_type in ['Hike', 'Run', 'Walk']:
        if activity_type in activities:
            output += _format_activity_section(activity_type, activities[activity_type])
            output += "\n"

    return output
