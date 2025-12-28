"""Strava authentication."""
import requests


def update_env_tokens(access_token, refresh_token, env_file='.env'):
    """Update .env file with new access and refresh tokens."""
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise RuntimeError(f"Environment file not found: {env_file}")
    except PermissionError:
        raise RuntimeError(f"Permission denied reading: {env_file}")

    access_token_found = False
    refresh_token_found = False
    updated_lines = []

    for line in lines:
        if line.startswith('STRAVA_ACCESS_TOKEN='):
            updated_lines.append(f'STRAVA_ACCESS_TOKEN={access_token}\n')
            access_token_found = True
        elif line.startswith('STRAVA_REFRESH_TOKEN='):
            updated_lines.append(f'STRAVA_REFRESH_TOKEN={refresh_token}\n')
            refresh_token_found = True
        else:
            updated_lines.append(line)

    if not access_token_found:
        raise RuntimeError(f"STRAVA_ACCESS_TOKEN not found in {env_file}")
    if not refresh_token_found:
        raise RuntimeError(f"STRAVA_REFRESH_TOKEN not found in {env_file}")

    try:
        with open(env_file, 'w') as f:
            f.writelines(updated_lines)
    except PermissionError:
        raise RuntimeError(f"Permission denied writing to: {env_file}")


def refresh_access_token(client_id, client_secret, refresh_token):
    """Refresh access token using refresh token."""
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Strava API token refresh failed with status {response.status_code}. "
            f"Response: {response.text}"
        )

    data = response.json()

    if 'access_token' not in data:
        raise RuntimeError(
            f"Strava API response missing 'access_token'. "
            f"Response keys: {list(data.keys())}"
        )

    return data
