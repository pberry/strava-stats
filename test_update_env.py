"""Tests for updating .env file with new tokens."""
import os
import tempfile
from auth import update_env_tokens


def test_update_env_tokens_replaces_access_and_refresh_tokens():
    """Updates STRAVA_ACCESS_TOKEN and STRAVA_REFRESH_TOKEN in .env file."""
    # Create temporary .env file with initial tokens
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("STRAVA_CLIENT_ID=12345\n")
        f.write("STRAVA_CLIENT_SECRET=secret123\n")
        f.write("STRAVA_ACCESS_TOKEN=old_access\n")
        f.write("STRAVA_REFRESH_TOKEN=old_refresh\n")
        temp_env_path = f.name

    try:
        # Update with new tokens
        update_env_tokens(
            access_token="new_access_token",
            refresh_token="new_refresh_token",
            env_file=temp_env_path
        )

        # Read file and verify tokens were updated
        with open(temp_env_path, 'r') as f:
            content = f.read()

        assert "STRAVA_ACCESS_TOKEN=new_access_token" in content
        assert "STRAVA_REFRESH_TOKEN=new_refresh_token" in content
        assert "STRAVA_CLIENT_ID=12345" in content  # Other values preserved
        assert "old_access" not in content
        assert "old_refresh" not in content

    finally:
        os.unlink(temp_env_path)
