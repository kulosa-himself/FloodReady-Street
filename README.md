# FloodReady Street

A student-built social-impact prototype for community waterlogging reports and hotspot awareness.

## Features
- Chennai-focused map with illustrative sample reports
- Submit a waterlogging report with location, severity and description
- Optional browser geolocation for coordinates
- SQLite storage for submitted reports
- Dashboard counts and recent-report table
- Reports clearly labelled as sample/unverified where appropriate

## Important limitations
This is a prototype, not an official emergency service. Initial map pins are illustrative sample data and must not be treated as live road conditions. It does not yet use live weather forecasts, automatically predict floods, or verify reports. Do not rely on it to decide whether a road is safe.

## Run locally
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

The SQLite database is created automatically as `floodready.db` on first run. It is excluded from Git by `.gitignore`.

## Tech stack
- Python + Flask
- SQLite
- HTML, CSS, JavaScript
- Leaflet + OpenStreetMap tiles

## Suggested next steps
- Add authentication and role-based access before deployment.
- Add report verification, expiry of stale reports, duplicate detection, and moderation.
- Integrate a reliable weather API and explain the risk calculation.
- Add tests and a privacy notice before collecting real users' data.
- Use official local guidance for emergency alerts.

## License
MIT. See `LICENSE`.
