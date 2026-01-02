# Strava Stats

A Python tool to sync your Strava activities to a local SQLite database and generate markdown reports for your hiking, running, and walking activities.

## Features

- OAuth 2.0 authentication with Strava API
- Automatic token refresh
- Incremental activity sync to SQLite database
- Generate yearly activity reports by type (Hikes, Runs, Walks)
- Markdown-formatted output (WordPress-ready)
- Monthly breakdown of miles and activity counts

## Prerequisites

- Python 3.7+
- A Strava account
- A Strava API application (see Setup below)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pberry/strava-stats.git
cd strava-stats
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Strava API Setup

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application if you haven't already
   - **Application Name**: Choose any name (e.g., "My Strava Stats")
   - **Category**: Choose the most appropriate (e.g., "Data Importer")
   - **Website**: Can be any URL (e.g., `http://localhost`)
3. Note your **Client ID** and **Client Secret**
4. **Important**: Set the **Authorization Callback Domain** to `localhost`
   - This allows the OAuth flow to redirect back to your local machine
   - No web server is needed - you'll just copy the code from the URL

## Configuration

### Initial Setup

1. Create a `.env` file in the project root:
```bash
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
STRAVA_ACCESS_TOKEN=
STRAVA_REFRESH_TOKEN=
```

2. Run the authorization script to get your access tokens:
```bash
python authorize.py
```

### OAuth Authorization Flow

The `authorize.py` script will guide you through the OAuth process:

1. **Visit the Authorization URL**: The script will display a URL. Open it in your browser.

2. **Authorize the App**: Strava will ask you to authorize the app with `activity:read` scope. Click "Authorize".

3. **Copy the Authorization Code**:
   - After authorization, Strava redirects to: `http://localhost/?code=XXXXX&scope=read,activity:read`
   - Your browser may show a "site can't be reached" error - **this is normal!**
   - Look at the URL in your browser's address bar
   - Copy the `XXXXX` part (the authorization code)

4. **Paste the Code**: Return to the terminal and paste the authorization code when prompted.

5. **Automatic Token Storage**: The script will:
   - Exchange the authorization code for access and refresh tokens
   - Automatically update your `.env` file with the tokens
   - You're now ready to sync activities!

### Token Refresh

Strava access tokens expire after 6 hours. This project handles token refresh automatically:

- **Automatic Refresh**: The `.env` file is automatically updated when tokens are refreshed
- **Manual Refresh**: If needed, you can manually refresh tokens:
  ```bash
  python refresh.py
  ```

You typically won't need to run the authorization process again unless you:
- Delete your `.env` file
- Revoke access in your [Strava settings](https://www.strava.com/settings/apps)
- Want to change the authorized scopes

## Usage

### Sync Activities

Sync your Strava activities to the local database:

```bash
python sync.py
```

On first run, this fetches all your activities. Subsequent runs only fetch new activities since the last sync.

The sync includes a 1-hour lookback window (configurable via `STRAVA_SYNC_LOOKBACK_SECONDS`) to catch activities that may have synced late from your device.

### Generate Reports

Generate a combined activity report for the current year:

```bash
python report.py
```

Generate a report for a specific year:

```bash
python report.py 2024
```

The report includes:
- Total miles and activity counts for Hikes, Runs, and Walks
- Monthly breakdown for each activity type
- Markdown formatting ready for WordPress or other platforms

Example output:
```markdown
# 2024 Activity Report

## Hikes
**Total:** 156.2 miles across 24 hikes

### Monthly Breakdown
- January: 12.3 miles (2 hikes)
- February: 15.7 miles (3 hikes)
...
```

## Project Structure

```
strava-stats/
├── authorize.py          # OAuth authorization CLI
├── refresh.py           # Token refresh CLI
├── sync.py              # Activity sync CLI
├── report.py            # Report generation CLI
├── auth.py              # OAuth token management
├── strava_api.py        # Strava API client
├── database.py          # SQLite database operations
├── activity_report.py   # Activity miles calculator
├── combined_report.py   # Multi-activity report formatter
├── markdown_formatter.py # Markdown output formatting
├── query_engine.py      # Activity filtering and aggregation
├── test_*.py            # Test files
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (not in git)
└── strava.db           # SQLite database (not in git)
```

## Testing

Run the test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

## Database Schema

The SQLite database (`strava.db`) contains:

- `activities` table: Stores activity metadata and full JSON payload
  - Indexed by `activity_id` (Strava's unique ID)
  - Includes: name, type, distance, moving_time, elapsed_time, elevation_gain, start_date
  - Full activity JSON stored in `json_data` column

- `metadata` table: Tracks sync state
  - `last_sync_timestamp`: Unix timestamp of last successful sync

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `STRAVA_CLIENT_ID` | Your Strava API client ID | Yes |
| `STRAVA_CLIENT_SECRET` | Your Strava API client secret | Yes |
| `STRAVA_ACCESS_TOKEN` | OAuth access token (expires after 6 hours, auto-refreshed) | Auto |
| `STRAVA_REFRESH_TOKEN` | OAuth refresh token (used to get new access tokens) | Auto |
| `STRAVA_SYNC_LOOKBACK_SECONDS` | Sync lookback window in seconds | No (default: 3600) |

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

This is a personal project, but feel free to fork and adapt it for your own use! See [CONTRIBUTING](CONTRIBUTING.md) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.
