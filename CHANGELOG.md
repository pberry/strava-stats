# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-02-28

### Added
- Automated weekly blog posting to WordPress via REST API
- Token manager with smart auto-refresh (only refreshes when expired)
- `STRAVA_TOKEN_EXPIRES_AT` tracking in .env for intelligent token refresh
- Individual activity query with date range and type filters
- Weekly report formatter with activity details (name, distance, time, elevation)
- WordPress client with HTTP Basic Auth (Application Passwords)
- Simple markdown-to-HTML converter for WordPress posting
- CLI orchestrator (`weekly_post.py`) — single entry point for cron automation
- `last_post_time` tracking in sync_metadata for incremental posting
- 27 new tests (total: 56)

### Changed
- `update_env_tokens()` now accepts optional `expires_at` parameter
- Token refresh is now automatic — no need to manually run `refresh.py`

### New Environment Variables
- `WP_URL` — WordPress site URL
- `WP_USERNAME` — WordPress username
- `WP_APP_PASSWORD` — WordPress Application Password
- `STRAVA_TOKEN_EXPIRES_AT` — managed automatically by token manager

### New Files
- `token_manager.py` — Smart token refresh (replaces manual `refresh.py` workflow)
- `weekly_report.py` — Weekly activity report formatter
- `wordpress.py` — WordPress REST API client
- `weekly_post.py` — Cron-ready CLI orchestrator

## [0.2.0] - 2026-01-01

### Added
- Comprehensive README.md with setup and usage instructions
- MIT LICENSE file
- CONTRIBUTING.md with contribution guidelines
- Detailed OAuth authorization flow documentation
- Token refresh documentation and usage instructions
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

### Changed
- Updated .gitignore to include .pytest_cache/, *.log, and .claude/

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
