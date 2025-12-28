"""Tests for fetching activities from Strava API."""
from unittest.mock import Mock, patch, call
from strava_api import fetch_activities


def test_fetch_activities_returns_list_of_activities():
    """Returns list of activity objects from Strava API."""
    # First page with 2 activities
    page1_response = Mock()
    page1_response.status_code = 200
    page1_response.json.return_value = [
        {'id': 123, 'name': 'Morning Run', 'type': 'Run'},
        {'id': 456, 'name': 'Evening Hike', 'type': 'Hike'}
    ]
    page1_response.headers = {
        'X-ReadRateLimit-Limit': '100,1000',
        'X-ReadRateLimit-Usage': '1,5'
    }

    # Second page empty (end of results)
    page2_response = Mock()
    page2_response.status_code = 200
    page2_response.json.return_value = []
    page2_response.headers = {
        'X-ReadRateLimit-Limit': '100,1000',
        'X-ReadRateLimit-Usage': '2,6'
    }

    with patch('strava_api.requests.get', side_effect=[page1_response, page2_response]):
        activities = fetch_activities(access_token='test_token')

    assert len(activities) == 2
    assert activities[0]['id'] == 123
    assert activities[1]['id'] == 456


def test_fetch_activities_handles_pagination():
    """Fetches all pages when API returns multiple pages."""
    # First page returns 2 activities
    page1_response = Mock()
    page1_response.status_code = 200
    page1_response.json.return_value = [
        {'id': 1, 'name': 'Activity 1'},
        {'id': 2, 'name': 'Activity 2'}
    ]
    page1_response.headers = {
        'X-ReadRateLimit-Limit': '100,1000',
        'X-ReadRateLimit-Usage': '1,5'
    }

    # Second page returns 2 activities
    page2_response = Mock()
    page2_response.status_code = 200
    page2_response.json.return_value = [
        {'id': 3, 'name': 'Activity 3'},
        {'id': 4, 'name': 'Activity 4'}
    ]
    page2_response.headers = {
        'X-ReadRateLimit-Limit': '100,1000',
        'X-ReadRateLimit-Usage': '2,6'
    }

    # Third page returns empty (no more activities)
    page3_response = Mock()
    page3_response.status_code = 200
    page3_response.json.return_value = []
    page3_response.headers = {
        'X-ReadRateLimit-Limit': '100,1000',
        'X-ReadRateLimit-Usage': '3,7'
    }

    with patch('strava_api.requests.get', side_effect=[page1_response, page2_response, page3_response]) as mock_get:
        activities = fetch_activities(access_token='test_token')

    # Should have made 3 API calls (pages 1, 2, 3)
    assert mock_get.call_count == 3

    # Should return all 4 activities from pages 1 and 2
    assert len(activities) == 4
    assert activities[0]['id'] == 1
    assert activities[3]['id'] == 4


def test_fetch_activities_fails_fast_on_api_error():
    """Raises RuntimeError when API returns error status code."""
    error_response = Mock()
    error_response.status_code = 401
    error_response.text = '{"message": "Unauthorized", "errors": [{"resource": "Athlete", "field": "access_token", "code": "invalid"}]}'

    with patch('strava_api.requests.get', return_value=error_response):
        try:
            fetch_activities(access_token='invalid_token')
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "401" in str(e)
            assert "Unauthorized" in str(e)
