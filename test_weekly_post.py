"""Tests for weekly post CLI orchestrator."""
import os
from datetime import date
from unittest.mock import patch, call
import pytest
from weekly_post import main, get_week_boundaries


class TestGetWeekBoundaries:
    """Tests for get_week_boundaries pure function."""

    def test_returns_monday_through_sunday_when_today_is_sunday(self):
        assert get_week_boundaries(date(2026, 3, 1)) == ('2026-02-23', '2026-03-01')

    def test_returns_same_day_as_start_when_today_is_monday(self):
        assert get_week_boundaries(date(2026, 2, 23)) == ('2026-02-23', '2026-03-01')

    def test_returns_correct_window_for_mid_week_day(self):
        assert get_week_boundaries(date(2026, 2, 25)) == ('2026-02-23', '2026-03-01')

    def test_handles_month_boundary_crossing(self):
        assert get_week_boundaries(date(2026, 3, 1)) == ('2026-02-23', '2026-03-01')

    def test_handles_year_boundary_crossing(self):
        assert get_week_boundaries(date(2025, 1, 1)) == ('2024-12-30', '2025-01-05')


def _mock_env():
    return {
        'STRAVA_CLIENT_ID': '12345',
        'STRAVA_CLIENT_SECRET': 'secret',
        'STRAVA_ACCESS_TOKEN': 'token',
        'STRAVA_REFRESH_TOKEN': 'refresh',
        'STRAVA_TOKEN_EXPIRES_AT': '9999999999',
        'WP_URL': 'https://blog.example.com',
        'WP_USERNAME': 'pat',
        'WP_APP_PASSWORD': 'xxxx',
    }


@patch('weekly_post.create_post')
@patch('weekly_post.format_weekly_report')
@patch('weekly_post.get_individual_activities')
@patch('weekly_post.sync_activities')
@patch('weekly_post.get_access_token')
def test_calls_pipeline_in_order(mock_token, mock_sync, mock_query, mock_format, mock_post):
    """Calls pipeline steps in correct order."""
    mock_token.return_value = 'access_token'
    mock_sync.return_value = 5
    mock_query.return_value = [{'type': 'Run', 'name': 'Test'}]
    mock_format.return_value = '# Report'
    mock_post.return_value = {'id': 1, 'link': 'https://blog.example.com/?p=1'}

    with patch.dict(os.environ, _mock_env(), clear=False):
        with patch('weekly_post.time.time', return_value=1740700800):
            result = main()

    assert result == 0
    mock_token.assert_called_once()
    mock_sync.assert_called_once()
    mock_query.assert_called_once()
    mock_format.assert_called_once()
    mock_post.assert_called_once()


@patch('weekly_post.create_post')
@patch('weekly_post.format_weekly_report')
@patch('weekly_post.get_individual_activities')
@patch('weekly_post.sync_activities')
@patch('weekly_post.get_access_token')
def test_uses_week_boundaries_not_last_post_time(mock_token, mock_sync, mock_query, mock_format, mock_post):
    """Uses Monday-Sunday week boundaries regardless of last_post_time."""
    mock_token.return_value = 'access_token'
    mock_sync.return_value = 0
    mock_query.return_value = [{'type': 'Run', 'name': 'Test'}]
    mock_format.return_value = '# Report'
    mock_post.return_value = {'id': 1, 'link': 'https://blog.example.com/?p=1'}

    # 2025-02-28 00:00:00 UTC is a Friday
    # Monday of that week = Feb 24, Sunday = Mar 2
    now = 1740700800

    with patch.dict(os.environ, _mock_env(), clear=False):
        with patch('weekly_post.time.time', return_value=now):
            main()

    query_call = mock_query.call_args
    assert query_call[1]['start_date'] == '2025-02-24'
    assert query_call[1]['end_date'] == '2025-03-02'


@patch('weekly_post.get_individual_activities')
@patch('weekly_post.sync_activities')
@patch('weekly_post.get_access_token')
def test_skips_posting_when_no_activities(mock_token, mock_sync, mock_query, capsys):
    """Skips posting when no activities found (returns 0)."""
    mock_token.return_value = 'access_token'
    mock_sync.return_value = 0
    mock_query.return_value = []

    with patch.dict(os.environ, _mock_env(), clear=False):
        with patch('weekly_post.time.time', return_value=1740700800):
            result = main()

    assert result == 0
    captured = capsys.readouterr()
    assert "No activities" in captured.out


@patch('weekly_post.get_access_token')
def test_returns_1_on_runtime_error(mock_token, capsys):
    """Returns 1 on RuntimeError."""
    mock_token.side_effect = RuntimeError("Token refresh failed")

    with patch.dict(os.environ, _mock_env(), clear=False):
        result = main()

    assert result == 1
    captured = capsys.readouterr()
    assert "Token refresh failed" in captured.err


@patch('weekly_post.create_post')
@patch('weekly_post.format_weekly_report')
@patch('weekly_post.get_individual_activities')
@patch('weekly_post.sync_activities')
@patch('weekly_post.get_access_token')
def test_prints_post_url_on_success(mock_token, mock_sync, mock_query, mock_format, mock_post, capsys):
    """Prints post URL on success."""
    mock_token.return_value = 'access_token'
    mock_sync.return_value = 1
    mock_query.return_value = [{'type': 'Run', 'name': 'Test'}]
    mock_format.return_value = '# Report'
    mock_post.return_value = {'id': 42, 'link': 'https://blog.example.com/?p=42'}

    with patch.dict(os.environ, _mock_env(), clear=False):
        with patch('weekly_post.time.time', return_value=1740700800):
            with patch('weekly_post._update_last_post_time'):
                main()

    captured = capsys.readouterr()
    assert "https://blog.example.com/?p=42" in captured.out


class TestDryRun:
    """Tests for --dry-run behaviour."""

    @patch('weekly_post.create_post')
    @patch('weekly_post.format_weekly_report')
    @patch('weekly_post.get_individual_activities')
    @patch('weekly_post.sync_activities')
    @patch('weekly_post.get_access_token')
    def test_dry_run_prints_report_without_posting(
        self, mock_token, mock_sync, mock_query, mock_format, mock_post, capsys
    ):
        """Dry-run prints title and report body, does not call create_post."""
        mock_token.return_value = 'access_token'
        mock_sync.return_value = 1
        mock_query.return_value = [{'type': 'Run', 'name': 'Morning Run'}]
        mock_format.return_value = '# Weekly report content'

        with patch.dict(os.environ, _mock_env(), clear=False):
            with patch('weekly_post.time.time', return_value=1740700800):
                result = main(dry_run=True)

        assert result == 0
        mock_post.assert_not_called()
        captured = capsys.readouterr()
        assert '[dry-run]' in captured.out
        assert '# Weekly report content' in captured.out

    @patch('weekly_post.format_weekly_report')
    @patch('weekly_post.get_individual_activities')
    @patch('weekly_post.sync_activities')
    @patch('weekly_post.get_access_token')
    def test_dry_run_does_not_update_last_post_time(
        self, mock_token, mock_sync, mock_query, mock_format
    ):
        """Dry-run does not persist last_post_time."""
        mock_token.return_value = 'access_token'
        mock_sync.return_value = 1
        mock_query.return_value = [{'type': 'Run', 'name': 'Morning Run'}]
        mock_format.return_value = '# Report'

        with patch.dict(os.environ, _mock_env(), clear=False):
            with patch('weekly_post.time.time', return_value=1740700800):
                with patch('weekly_post._update_last_post_time') as mock_update:
                    main(dry_run=True)

        mock_update.assert_not_called()

    @patch('weekly_post.format_weekly_report')
    @patch('weekly_post.get_individual_activities')
    @patch('weekly_post.sync_activities')
    @patch('weekly_post.get_access_token')
    def test_dry_run_still_syncs_and_formats(
        self, mock_token, mock_sync, mock_query, mock_format
    ):
        """Dry-run still syncs activities and formats the report."""
        mock_token.return_value = 'access_token'
        mock_sync.return_value = 2
        mock_query.return_value = [{'type': 'Run', 'name': 'Morning Run'}]
        mock_format.return_value = '# Report'

        with patch.dict(os.environ, _mock_env(), clear=False):
            with patch('weekly_post.time.time', return_value=1740700800):
                main(dry_run=True)

        mock_sync.assert_called_once()
        mock_format.assert_called_once()
