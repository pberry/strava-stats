"""Tests for token manager with auto-refresh."""
import os
import tempfile
from unittest.mock import patch
import pytest
from token_manager import get_access_token


def _create_temp_env(lines):
    """Create a temporary .env file with the given lines."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        for line in lines:
            f.write(line + '\n')
        return f.name


def _base_env_lines():
    return [
        "STRAVA_CLIENT_ID=12345",
        "STRAVA_CLIENT_SECRET=secret123",
        "STRAVA_ACCESS_TOKEN=valid_token",
        "STRAVA_REFRESH_TOKEN=refresh_token",
    ]


def test_returns_existing_token_when_not_expired():
    """Returns existing access token when expires_at is in the future."""
    env_path = _create_temp_env(
        _base_env_lines() + ["STRAVA_TOKEN_EXPIRES_AT=9999999999"]
    )

    try:
        with patch('token_manager.time.time', return_value=1700000000):
            token = get_access_token(env_file=env_path)

        assert token == "valid_token"
    finally:
        os.unlink(env_path)


def test_refreshes_when_expired():
    """Refreshes and updates .env when expires_at is in the past."""
    env_path = _create_temp_env(
        _base_env_lines() + ["STRAVA_TOKEN_EXPIRES_AT=1000000"]
    )

    mock_response = {
        'access_token': 'new_access',
        'refresh_token': 'new_refresh',
        'expires_at': 1700003600,
    }

    try:
        with patch('token_manager.time.time', return_value=1700000000):
            with patch('token_manager.refresh_access_token', return_value=mock_response):
                token = get_access_token(env_file=env_path)

        assert token == "new_access"

        with open(env_path, 'r') as f:
            content = f.read()
        assert "STRAVA_ACCESS_TOKEN=new_access" in content
        assert "STRAVA_REFRESH_TOKEN=new_refresh" in content
        assert "STRAVA_TOKEN_EXPIRES_AT=1700003600" in content
    finally:
        os.unlink(env_path)


def test_refreshes_when_expires_at_missing():
    """Refreshes when STRAVA_TOKEN_EXPIRES_AT is missing from .env."""
    env_path = _create_temp_env(_base_env_lines())

    mock_response = {
        'access_token': 'new_access',
        'refresh_token': 'new_refresh',
        'expires_at': 1700003600,
    }

    try:
        with patch('token_manager.refresh_access_token', return_value=mock_response):
            token = get_access_token(env_file=env_path)

        assert token == "new_access"
    finally:
        os.unlink(env_path)


def test_refreshes_within_buffer_window():
    """Refreshes when token expires within buffer window (default 5 min)."""
    expires_in_3_minutes = 1700000180
    env_path = _create_temp_env(
        _base_env_lines() + [f"STRAVA_TOKEN_EXPIRES_AT={expires_in_3_minutes}"]
    )

    mock_response = {
        'access_token': 'new_access',
        'refresh_token': 'new_refresh',
        'expires_at': 1700003600,
    }

    try:
        with patch('token_manager.time.time', return_value=1700000000):
            with patch('token_manager.refresh_access_token', return_value=mock_response):
                token = get_access_token(env_file=env_path)

        assert token == "new_access"
    finally:
        os.unlink(env_path)


def test_raises_when_credentials_missing():
    """Raises RuntimeError when credentials missing from .env."""
    env_path = _create_temp_env([
        "STRAVA_ACCESS_TOKEN=valid_token",
    ])

    try:
        env_clean = {k: v for k, v in os.environ.items()
                     if not k.startswith('STRAVA_')}
        with patch.dict(os.environ, env_clean, clear=True):
            with pytest.raises(RuntimeError, match="STRAVA_CLIENT_ID not found"):
                get_access_token(env_file=env_path)
    finally:
        os.unlink(env_path)
