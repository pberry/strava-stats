# PRD: Strava Stats Reporter

**Status:** Approved

## 1. Problem

Strava's web UI doesn't answer specific questions about activity data. Simple queries like "how many hiking miles in 2025" require manual calculation or aren't possible at all. A spreadsheet would be more useful than Strava's built-in interface for answering these questions.

**Who has this problem:** Personal use—one Strava user who wants to interrogate their own activity data.

**Why it matters:** End-of-year reflection and ongoing activity tracking require flexible querying that Strava doesn't provide.

## 2. Design Principles

**Boring technology.** This is not a technology project—it's about getting information. Choose simple, proven tools.

**Be a good API citizen.** Store data locally to stay under Strava API quotas. Sync incrementally (only fetch new activities) rather than re-fetching everything.

**On-demand, not real-time.** Reports run when requested, not continuously.

## 3. What We're Building

### Data Acquisition
- Authenticate with Strava API using OAuth (Client ID + Access/Refresh tokens)
- Handle token refresh (access token expires, refresh token available)
- Fetch ALL activity types from Strava API
- Support arbitrary date ranges (not limited to 2025)
- Store activities locally in SQLite
- Respect API rate limits:
  - Read rate limits: 100 requests per 15 minutes, 1,000 daily
  - Overall rate limits: 200 requests per 15 minutes, 2,000 daily

### Incremental Sync
- Remember where we left off (last sync timestamp or activity ID)
- On subsequent syncs, only fetch new activities
- Update local database with new data

### Data Storage
- SQLite database storing the complete activity payload from Strava API
- Store everything the API returns (not just selected fields)
- This ensures future reports can query any field without re-fetching

### Reporting
- Python scripts to generate reports
- Reports focus on: **mileage, time, and elevation**
- Differentiate by activity type (runs vs hikes vs walks)
- Differentiate by tags (e.g., "Long Run" vs regular runs)
- Support arbitrary date ranges for queries
- Output format: Markdown (for pasting into WordPress)
- Reports are generated on-demand

### Error Handling
- If Strava API is down or returns an error: print the error code and stop gracefully
- Simple error reporting (no complex retry logic initially)

### Initial Report
- "How many hiking miles in 2025?"

## 4. What We're NOT Building

- Fancy visualizations or charts
- Editing or modifying Strava data (read-only)
- Real-time dashboards
- Social features
- Multi-user support

## 5. Success Criteria

**Primary:** Can answer "how many miles hiked in 2025" by running a report.

**Secondary indicators of success:**
- Stays under Strava API rate limits
- Incremental sync works (doesn't re-fetch all data every time)
- Easy to add new reports for other questions (mileage, time, elevation queries)

## 6. Milestones

### M1: Data Acquisition
**What's delivered:** Can authenticate with Strava, fetch activities, and store them in SQLite.

#### Deliverables

**D1.1: Project Setup**
- Acceptance criteria:
  - Python virtual environment created
  - Dependencies documented (requests, sqlite3, etc.)
  - `.env` file for storing API credentials (Client ID, Client Secret, Access Token, Refresh Token)
  - `.gitignore` excludes `.env` and database files
  - Project structure follows Python best practices
- Verification: Can activate venv, dependencies install cleanly

**D1.2: Strava OAuth Authentication**
- Acceptance criteria:
  - Read credentials from `.env`
  - Use Access Token for API requests
  - Detect when Access Token is expired
  - Refresh Access Token using Refresh Token
  - Update `.env` with new Access Token after refresh
- Verification: Can make authenticated API call, token refresh works when forced

**D1.3: Fetch Activities from API**
- Acceptance criteria:
  - Call Strava API to fetch activities for a given date range
  - Handle pagination (Strava returns activities in pages)
  - Respect rate limits (100 read requests per 15 min)
  - Print error code if API fails
  - Return list of activity objects
- Verification: Can fetch all 2025 activities without hitting rate limits

**D1.4: SQLite Database Storage**
- Acceptance criteria:
  - Create SQLite database if it doesn't exist
  - Schema stores complete activity payload as JSON
  - Store activity ID, date, type, distance, time, elevation, and full JSON payload
  - Insert activities without duplicates (upsert by activity ID)
- Verification: After fetch, database contains all activities with queryable fields

---

### M2: Incremental Sync
**What's delivered:** Subsequent syncs only fetch new activities, not everything.

#### Deliverables

**D2.1: Track Last Sync**
- Acceptance criteria:
  - Store last sync timestamp in database or config file
  - On first sync, no timestamp exists (fetch from specified start date)
  - On subsequent syncs, use last sync timestamp as "after" parameter
- Verification: Second sync only fetches activities created since first sync

**D2.2: Sync Command**
- Acceptance criteria:
  - Python script `sync.py` that runs the sync process
  - Accepts optional date range arguments (start_date, end_date)
  - If no arguments, syncs from last sync timestamp to now
  - Updates last sync timestamp after successful sync
- Verification: Running `sync.py` twice doesn't re-fetch same activities

---

### M3: Basic Reporting
**What's delivered:** Can answer "how many hiking miles in 2025" with a Markdown report.

#### Deliverables

**D3.1: Query Engine**
- Acceptance criteria:
  - Python module to query SQLite database
  - Filter by date range (start_date, end_date)
  - Filter by activity type (e.g., "Hike", "Run", "Walk")
  - Filter by tags/keywords in activity name
  - Return aggregated metrics: total distance, total time, total elevation
- Verification: Can query database for hiking activities in 2025 and get correct totals

**D3.2: Hiking Miles Report**
- Acceptance criteria:
  - Python script `report_hiking_miles.py`
  - Accepts year as argument (defaults to current year)
  - Queries database for hiking activities in that year
  - Calculates total miles (convert meters to miles if needed)
  - Outputs result
- Verification: Running script for 2025 returns accurate hiking mileage

**D3.3: Markdown Formatter**
- Acceptance criteria:
  - Format report output as Markdown
  - Include: title, total miles, breakdown by month
  - Output can be copy-pasted directly into WordPress
- Verification: Output is valid Markdown, looks good when pasted into WordPress

---

## 7. Timeline

**M1: Data Acquisition** - Foundation for everything else
**M2: Incremental Sync** - Makes it practical for ongoing use
**M3: Basic Reporting** - Delivers the value (answers the question)
