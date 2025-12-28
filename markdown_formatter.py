"""Markdown report formatter."""


def _format_monthly_line(month_data):
    """Format a single month's data as markdown line."""
    month = month_data['month']
    miles = month_data['miles']
    count = month_data['count']
    return f"**{month}:** {miles} miles ({count} hikes)\n"


def _format_monthly_section(monthly_breakdown):
    """Format monthly breakdown section."""
    lines = [_format_monthly_line(month_data) for month_data in monthly_breakdown]
    return "\n## Monthly Breakdown\n\n" + "".join(lines)


def format_hiking_report(report_data):
    """Format hiking report as markdown."""
    required_fields = ['year', 'total_miles', 'activity_count']
    for field in required_fields:
        if field not in report_data:
            raise ValueError(
                f"Expected '{field}' in report_data, but it was not found. "
                f"Available keys: [{', '.join(report_data.keys())}]"
            )

    year = report_data['year']
    total_miles = report_data['total_miles']
    activity_count = report_data['activity_count']

    output = f"""# {year} Hiking Report

**Total Miles:** {total_miles}
**Total Hikes:** {activity_count}
"""

    if 'monthly_breakdown' in report_data:
        output += _format_monthly_section(report_data['monthly_breakdown'])

    return output
