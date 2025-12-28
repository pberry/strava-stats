"""Tests for combined activity report formatter."""
from combined_report import format_combined_report


def test_format_combined_report_includes_all_activity_types():
    """Formats multiple activity types in single markdown report."""
    report_data = {
        'year': 2025,
        'activities': {
            'Hike': {
                'total_miles': 42.5,
                'activity_count': 8,
                'monthly_breakdown': [
                    {'month': 'January', 'miles': 15.2, 'count': 3}
                ]
            },
            'Run': {
                'total_miles': 125.0,
                'activity_count': 25,
                'monthly_breakdown': [
                    {'month': 'January', 'miles': 50.0, 'count': 10}
                ]
            },
            'Walk': {
                'total_miles': 30.5,
                'activity_count': 12,
                'monthly_breakdown': [
                    {'month': 'January', 'miles': 10.5, 'count': 4}
                ]
            }
        }
    }

    result = format_combined_report(report_data)

    # Check title
    assert '# 2025 Activity Report' in result

    # Check each activity type section
    assert '## Hikes' in result
    assert '**Total Miles:** 42.5' in result
    assert '**Total Hikes:** 8' in result

    assert '## Runs' in result
    assert '**Total Miles:** 125.0' in result
    assert '**Total Runs:** 25' in result

    assert '## Walks' in result
    assert '**Total Miles:** 30.5' in result
    assert '**Total Walks:** 12' in result

    # Check monthly breakdown appears
    assert '### Monthly Breakdown' in result
    assert '**January:** 15.2 miles (3 hikes)' in result
    assert '**January:** 50.0 miles (10 runs)' in result
