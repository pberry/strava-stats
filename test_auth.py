"""Tests for Strava authentication."""
import os
from dotenv import load_dotenv


def test_refresh_token_returns_access_token():
    """Returns new access token when refreshing with valid refresh token."""
    load_dotenv()

    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    from auth import refresh_access_token

    result = refresh_access_token(client_id, client_secret, refresh_token)

    assert 'access_token' in result
    assert len(result['access_token']) > 0
