#!/usr/bin/env python3
"""
Refresh Strava API tokens and update .env file.

This script reads your current refresh token from .env, requests new
access and refresh tokens from Strava, and updates .env with the new values.
"""
import sys
from refresh_tokens import refresh_and_save_tokens


def main():
    """Main entry point."""
    try:
        print("Refreshing Strava tokens...")
        refresh_and_save_tokens()
        print("✓ Tokens refreshed and saved to .env")
        return 0
    except RuntimeError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
