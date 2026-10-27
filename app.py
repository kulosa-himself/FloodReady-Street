from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "floodready.db"
app = Flask(__name__)
app.secret_key = "change-this-for-deployment"

SAMPLE_REPORTS = [
    ("T. Nagar Main Road", 13.0418, 80.2337, "High", "Sample report: water covering part of the road", "2026-10-26 17:30"),
    ("Velachery Bypass Road", 12.9750, 80.2212, "Medium", "Sample report: slow-moving water near junction", "2026-10-26 16:45"),
    ("Perambur High Road", 13.1167, 80.2330, "High", "Sample report: recurring waterlogging after rain", "2026-10-26 15:50"),
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Unverified'
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        if count == 0:
            conn.executemany("""
                INSERT INTO reports (location, latitude, longitude, severity, description, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Sample')
            """, SAMPLE_REPORTS)

@app.route("/")
def index():
    with get_db() as conn:
        reports = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
    total = len(reports)
    high = sum(1 for r in reports if r["severity"] == "High")
    pending = sum(1 for r in reports if r["status"] in ("Unverified", "Pending"))
    return render_template("index.html", reports=reports, total=total, high=high, pending=pending)

@app.route("/report", methods=["POST"])
def report():
    location = request.form.get("location", "").strip()
    description = request.form.get("description", "").strip()
    severity = request.form.get("severity", "Medium")
    lat = request.form.get("latitude", "").strip()
    lon = request.form.get("longitude", "").strip()

    if not location or not description:
        flash("Please provide a location and description.", "error")
        return redirect(url_for("index"))

    if severity not in ("Low", "Medium", "High"):
        severity = "Medium"

    try:
        latitude = float(lat) if lat else None
        longitude = float(lon) if lon else None
    except ValueError:
        latitude = longitude = None

    with get_db() as conn:
        conn.execute("""
            INSERT INTO reports (location, latitude, longitude, severity, description, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Unverified')
        """, (location, latitude, longitude, severity, description,
              datetime.now().strftime("%Y-%m-%d %H:%M")))
    flash("Report saved. It is marked unverified until checked.", "success")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok", "project": "FloodReady Street"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
