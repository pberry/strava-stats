"""Tests for weekly post CLI orchestrator."""
import os
import tempfile
from unittest.mock import patch, MagicMock, call
import pytest
from weekly_post import main


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
            with patch('weekly_post._get_last_post_time', return_value=None):
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
def test_defaults_to_7_days_ago_when_no_last_post(mock_token, mock_sync, mock_query, mock_format, mock_post):
    """Defaults to 7 days ago when no last_post_time exists."""
    mock_token.return_value = 'access_token'
    mock_sync.return_value = 0
    mock_query.return_value = [{'type': 'Run', 'name': 'Test'}]
    mock_format.return_value = '# Report'
    mock_post.return_value = {'id': 1, 'link': 'https://blog.example.com/?p=1'}

    now = 1740700800  # 2025-02-28 00:00:00 UTC

    with patch.dict(os.environ, _mock_env(), clear=False):
        with patch('weekly_post.time.time', return_value=now):
            with patch('weekly_post._get_last_post_time', return_value=None):
                main()

    query_call = mock_query.call_args
    assert query_call[1]['start_date'] is not None


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
            with patch('weekly_post._get_last_post_time', return_value=None):
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
            with patch('weekly_post._get_last_post_time', return_value=None):
                with patch('weekly_post._update_last_post_time'):
                    main()

    captured = capsys.readouterr()
    assert "https://blog.example.com/?p=42" in captured.out
