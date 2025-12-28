"""Strava API client for fetching activities."""
import requests


BASE_URL = 'https://www.strava.com/api/v3'
PER_PAGE = 30


def _fetch_activities_page(access_token, page, after=None, before=None):
    """Fetch a single page of activities from Strava API."""
    params = {'page': page, 'per_page': PER_PAGE}
    if after:
        params['after'] = after
    if before:
        params['before'] = before

    response = requests.get(
        f'{BASE_URL}/athlete/activities',
        headers={'Authorization': f'Bearer {access_token}'},
        params=params
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Strava API request failed with status {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()


def fetch_activities(access_token, after=None, before=None):
    """Fetch all activities from Strava API with pagination."""
    all_activities = []
    page = 1

    while True:
        activities = _fetch_activities_page(access_token, page, after, before)

        if not activities:
            break

        all_activities.extend(activities)
        page += 1

    return all_activities
