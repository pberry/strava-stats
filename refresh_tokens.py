"""Script to refresh Strava tokens and update .env file."""
import os
from dotenv import load_dotenv
from auth import refresh_access_token, update_env_tokens


def refresh_and_save_tokens(env_file='.env'):
    """Refresh tokens from Strava API and save to .env file."""
    load_dotenv(env_file)

    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    if not client_id:
        raise RuntimeError(f"STRAVA_CLIENT_ID not found in {env_file}")
    if not client_secret:
        raise RuntimeError(f"STRAVA_CLIENT_SECRET not found in {env_file}")
    if not refresh_token:
        raise RuntimeError(f"STRAVA_REFRESH_TOKEN not found in {env_file}")

    token_data = refresh_access_token(client_id, client_secret, refresh_token)

    update_env_tokens(
        access_token=token_data['access_token'],
        refresh_token=token_data['refresh_token'],
        env_file=env_file
    )
