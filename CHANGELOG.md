# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Strava API authentication with OAuth token refresh
- Automatic token refresh and .env file updates
- Activity fetching from Strava API with pagination support
- Comprehensive error handling with fail-fast principle
- CLI script for manual token refresh (`refresh.py`)
- Full test suite with pytest
- Python virtual environment setup
- Git repository initialization

### Technical Details
- `auth.py`: OAuth token refresh and .env file management
- `strava_api.py`: Activity fetching with automatic pagination
- `refresh_tokens.py`: Integration for refresh and save workflow
- All functions include fail-fast error handling
- Test coverage for all core functionality

## [0.1.0] - Unreleased

Initial project setup and authentication foundation.
