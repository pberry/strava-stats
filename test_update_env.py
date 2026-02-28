"""Tests for updating .env file with new tokens."""
import os
import tempfile
from auth import update_env_tokens


def _create_temp_env(lines):
    """Create a temporary .env file with the given lines."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        for line in lines:
            f.write(line + '\n')
        return f.name


def _read_temp_env(path):
    """Read and return the contents of a temporary .env file."""
    with open(path, 'r') as f:
        return f.read()


def test_update_env_tokens_replaces_access_and_refresh_tokens():
    """Updates STRAVA_ACCESS_TOKEN and STRAVA_REFRESH_TOKEN in .env file."""
    temp_env_path = _create_temp_env([
        "STRAVA_CLIENT_ID=12345",
        "STRAVA_CLIENT_SECRET=secret123",
        "STRAVA_ACCESS_TOKEN=old_access",
        "STRAVA_REFRESH_TOKEN=old_refresh",
    ])

    try:
        update_env_tokens(
            access_token="new_access_token",
            refresh_token="new_refresh_token",
            env_file=temp_env_path
        )

        content = _read_temp_env(temp_env_path)
        assert "STRAVA_ACCESS_TOKEN=new_access_token" in content
        assert "STRAVA_REFRESH_TOKEN=new_refresh_token" in content
        assert "STRAVA_CLIENT_ID=12345" in content
        assert "old_access" not in content
        assert "old_refresh" not in content
    finally:
        os.unlink(temp_env_path)


def test_writes_expires_at_when_provided():
    """Writes STRAVA_TOKEN_EXPIRES_AT to .env when expires_at param provided."""
    temp_env_path = _create_temp_env([
        "STRAVA_CLIENT_ID=12345",
        "STRAVA_CLIENT_SECRET=secret123",
        "STRAVA_ACCESS_TOKEN=old_access",
        "STRAVA_REFRESH_TOKEN=old_refresh",
        "STRAVA_TOKEN_EXPIRES_AT=1000000",
    ])

    try:
        update_env_tokens(
            access_token="new_access",
            refresh_token="new_refresh",
            expires_at=1700000000,
            env_file=temp_env_path
        )

        content = _read_temp_env(temp_env_path)
        assert "STRAVA_TOKEN_EXPIRES_AT=1700000000" in content
        assert "1000000" not in content.replace("1700000000", "")
    finally:
        os.unlink(temp_env_path)


def test_appends_expires_at_when_line_missing():
    """Appends STRAVA_TOKEN_EXPIRES_AT when not already in .env."""
    temp_env_path = _create_temp_env([
        "STRAVA_CLIENT_ID=12345",
        "STRAVA_CLIENT_SECRET=secret123",
        "STRAVA_ACCESS_TOKEN=old_access",
        "STRAVA_REFRESH_TOKEN=old_refresh",
    ])

    try:
        update_env_tokens(
            access_token="new_access",
            refresh_token="new_refresh",
            expires_at=1700000000,
            env_file=temp_env_path
        )

        content = _read_temp_env(temp_env_path)
        assert "STRAVA_TOKEN_EXPIRES_AT=1700000000" in content
    finally:
        os.unlink(temp_env_path)


def test_backward_compatible_without_expires_at():
    """Works without expires_at param — no change to .env for that key."""
    temp_env_path = _create_temp_env([
        "STRAVA_CLIENT_ID=12345",
        "STRAVA_CLIENT_SECRET=secret123",
        "STRAVA_ACCESS_TOKEN=old_access",
        "STRAVA_REFRESH_TOKEN=old_refresh",
        "STRAVA_TOKEN_EXPIRES_AT=1000000",
    ])

    try:
        update_env_tokens(
            access_token="new_access",
            refresh_token="new_refresh",
            env_file=temp_env_path
        )

        content = _read_temp_env(temp_env_path)
        assert "STRAVA_TOKEN_EXPIRES_AT=1000000" in content
        assert "STRAVA_ACCESS_TOKEN=new_access" in content
    finally:
        os.unlink(temp_env_path)
