"""Integration test for refresh and save workflow."""
import os
import tempfile
from unittest.mock import patch
from refresh_tokens import refresh_and_save_tokens


def test_refresh_and_save_updates_env_file_with_new_tokens():
    """Refreshes tokens from API and saves them to .env file."""
    # Create temp .env with initial values
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("STRAVA_CLIENT_ID=12345\n")
        f.write("STRAVA_CLIENT_SECRET=secret123\n")
        f.write("STRAVA_ACCESS_TOKEN=old_access\n")
        f.write("STRAVA_REFRESH_TOKEN=old_refresh\n")
        temp_env = f.name

    try:
        # Mock the API call to return new tokens
        mock_response = {
            'access_token': 'new_access_123',
            'refresh_token': 'new_refresh_456',
            'expires_at': 1234567890
        }

        with patch('refresh_tokens.refresh_access_token', return_value=mock_response):
            refresh_and_save_tokens(env_file=temp_env)

        # Verify .env was updated with new tokens
        with open(temp_env, 'r') as f:
            content = f.read()

        assert 'STRAVA_ACCESS_TOKEN=new_access_123' in content
        assert 'STRAVA_REFRESH_TOKEN=new_refresh_456' in content
        assert 'old_access' not in content
        assert 'old_refresh' not in content

    finally:
        os.unlink(temp_env)
