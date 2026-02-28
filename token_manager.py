"""Token manager with auto-refresh for Strava API."""
import os
import time
from dotenv import load_dotenv
from auth import refresh_access_token, update_env_tokens


REFRESH_BUFFER_SECONDS = 300


def get_access_token(env_file='.env'):
    """Return a valid access token, refreshing if needed."""
    load_dotenv(env_file, override=True)

    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
    access_token = os.getenv('STRAVA_ACCESS_TOKEN')

    if not client_id:
        raise RuntimeError(f"STRAVA_CLIENT_ID not found in {env_file}")
    if not client_secret:
        raise RuntimeError(f"STRAVA_CLIENT_SECRET not found in {env_file}")
    if not refresh_token:
        raise RuntimeError(f"STRAVA_REFRESH_TOKEN not found in {env_file}")

    expires_at_str = os.getenv('STRAVA_TOKEN_EXPIRES_AT')
    token_expired = True

    if expires_at_str:
        expires_at = int(expires_at_str)
        token_expired = time.time() + REFRESH_BUFFER_SECONDS >= expires_at

    if not token_expired:
        return access_token

    token_data = refresh_access_token(client_id, client_secret, refresh_token)

    update_env_tokens(
        access_token=token_data['access_token'],
        refresh_token=token_data['refresh_token'],
        expires_at=token_data.get('expires_at'),
        env_file=env_file
    )

    return token_data['access_token']
