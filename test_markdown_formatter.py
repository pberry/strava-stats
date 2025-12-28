"""Tests for markdown report formatter."""
import pytest
from markdown_formatter import format_hiking_report


def test_format_hiking_report_creates_markdown_with_title_and_total():
    """Produces markdown with title and total miles summary."""
    report_data = {
        'year': 2025,
        'total_miles': 42.5,
        'activity_count': 8
    }

    result = format_hiking_report(report_data)

    assert '# 2025 Hiking Report' in result
    assert '**Total Miles:** 42.5' in result
    assert '**Total Hikes:** 8' in result


def test_format_hiking_report_raises_error_when_required_field_missing():
    """Raises ValueError when required field is missing from report_data."""
    incomplete_data = {
        'year': 2025,
        'total_miles': 42.5
        # missing activity_count
    }

    with pytest.raises(ValueError, match="Expected 'activity_count' in report_data"):
        format_hiking_report(incomplete_data)


def test_format_hiking_report_includes_monthly_breakdown():
    """Includes breakdown by month in markdown output."""
    report_data = {
        'year': 2025,
        'total_miles': 42.5,
        'activity_count': 8,
        'monthly_breakdown': [
            {'month': 'January', 'miles': 15.2, 'count': 3},
            {'month': 'February', 'miles': 27.3, 'count': 5}
        ]
    }

    result = format_hiking_report(report_data)

    assert '## Monthly Breakdown' in result
    assert '**January:** 15.2 miles (3 hikes)' in result
    assert '**February:** 27.3 miles (5 hikes)' in result
