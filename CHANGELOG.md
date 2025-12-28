# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Strava API authentication with OAuth token refresh
- Automatic token refresh and .env file updates
- Activity fetching from Strava API with pagination support
- SQLite database for storing activities with extracted fields and full JSON
- Incremental sync with last sync timestamp tracking
- Query engine for filtering and aggregating activities
- Activity miles reports with meter-to-mile conversion and monthly breakdown (Hikes, Runs, Walks)
- Combined activity report showing all activity types in single document
- Markdown formatter for WordPress-ready report output
- CLI scripts: `authorize.py` for OAuth setup, `refresh.py` for token refresh, `sync.py` for activity sync, `report.py` for combined reports
- Comprehensive error handling with fail-fast principle
- Full test suite with pytest (21 tests)
- Python virtual environment setup
- Git repository initialization

### Technical Details
- `auth.py`: OAuth token refresh, authorization code exchange, and .env file management
- `authorize.py`: Interactive CLI script for OAuth authorization with activity:read scope
- `strava_api.py`: Activity fetching with automatic pagination
- `database.py`: SQLite storage with extracted fields + complete JSON payload
  - Metadata table for tracking last sync timestamp
  - Upsert by activity_id prevents duplicates
- `sync.py`: Incremental sync - fetches only new activities since last sync
- `query_engine.py`: Filter by type, date range; aggregate distance, time, elevation
- `activity_report.py`: Generic activity miles calculator for any activity type
  - Month-by-month aggregation with proper date boundaries
  - Leap year handling for February
- `hiking_report.py`: Convenience wrapper around activity_report for hiking
- `combined_report.py`: Format multiple activity types in single markdown report
- `report.py`: CLI script to generate combined Hike/Run/Walk reports
- `markdown_formatter.py`: Format hiking reports as Markdown
  - Title, total miles, total hikes
  - Monthly breakdown section (optional)
  - WordPress-compatible output
- `refresh_tokens.py`: Integration for refresh and save workflow
- All functions include fail-fast error handling
- Context managers for safe resource handling
- Complete test coverage for all functionality

## [0.1.0] - Unreleased

Initial project setup and authentication foundation.
