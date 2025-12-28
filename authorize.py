#!/usr/bin/env python3
"""Interactive OAuth authorization script for Strava.

This script helps you authorize the app with the correct scopes
to read activity data from Strava.
"""
import os
from dotenv import load_dotenv
from auth import exchange_code_for_tokens, update_env_tokens


def main():
    """Run interactive OAuth authorization flow."""
    load_dotenv()

    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    if not client_id or not client_secret:
        print('✗ Error: STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET must be set in .env')
        return 1

    # Construct authorization URL with activity:read scope
    redirect_uri = 'http://localhost'
    scope = 'activity:read'
    auth_url = (
        f'https://www.strava.com/oauth/authorize'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&response_type=code'
        f'&scope={scope}'
    )

    print('=' * 70)
    print('Strava OAuth Authorization')
    print('=' * 70)
    print()
    print('Step 1: Visit this URL in your browser:')
    print()
    print(auth_url)
    print()
    print('Step 2: Authorize the app (click "Authorize")')
    print()
    print('Step 3: You\'ll be redirected to a URL like:')
    print(f'        {redirect_uri}/?code=XXXXX&scope=read,activity:read')
    print()
    print('        Copy the XXXXX code from the URL.')
    print()
    print('=' * 70)
    print()

    # Get authorization code from user
    auth_code = input('Paste the authorization code here: ').strip()

    if not auth_code:
        print('✗ Error: No authorization code provided')
        return 1

    print()
    print('Exchanging authorization code for tokens...')

    try:
        token_data = exchange_code_for_tokens(client_id, client_secret, auth_code)
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']

        print('✓ Token exchange successful')
        print()
        print('Updating .env file with new tokens...')

        update_env_tokens(access_token, refresh_token)

        print('✓ .env file updated')
        print()
        print('=' * 70)
        print('Authorization complete! You can now run sync.py')
        print('=' * 70)

        return 0

    except RuntimeError as e:
        print(f'✗ Error: {e}')
        return 1
    except Exception as e:
        print(f'✗ Unexpected error: {e}')
        return 1


if __name__ == '__main__':
    exit(main())
