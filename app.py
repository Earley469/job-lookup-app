import sqlite3
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Job / Serial Lookup")
templates = Jinja2Templates(directory="templates")

DB_PATH = "local_data.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            record_type TEXT NOT NULL,
            job_number TEXT,
            serial_number TEXT,
            summary TEXT,
            status TEXT,
            details TEXT,
            source_url TEXT
        )
    """)
    conn.commit()

    # Seed with example data only if table is empty
    count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    if count == 0:
        sample_data = [
            (
                "Manufacturing DB",
                "work_order",
                "JOB-1001",
                "SN-ABC-2001",
                "Motor assembly completed",
                "Complete",
                json.dumps({
                    "station": "Assembly A",
                    "operator": "J. Smith",
                    "date": "2026-09-10"
                }),
                "http://local-system/workorder/1001"
            ),
            (
                "Inventory System",
                "parts",
                "JOB-1001",
                "SN-ABC-2001",
                "Part replaced during service",
                "In Service",
                json.dumps({
                    "part_number": "P-4452",
                    "vendor": "Acme Components"
                }),
                "http://local-system/parts/4452"
            ),
            (
                "Quality DB",
                "inspection",
                "JOB-2204",
                "SN-XYZ-9901",
                "Final quality test passed",
                "Passed",
                json.dumps({
                    "inspector": "R. Lee",
                    "test": "Leak Test",
                    "result": "Pass"
                }),
                "http://local-system/inspection/9901"
            ),
            (
                "Shipping System",
                "shipment",
                "JOB-2204",
                "SN-XYZ-9901",
                "Delivered to customer",
                "Shipped",
                json.dumps({
                    "carrier": "UPS",
                    "tracking": "1ZABC123"
                }),
                "http://local-system/shipment/1ZABC123"
            ),
            (
                "Service Log",
                "service_record",
                "JOB-3007",
                "SN-DEF-7784",
                "Replacement completed in field service",
                "Closed",
                json.dumps({
                    "technician": "M. Gomez",
                    "service_date": "2026-09-11"
                }),
                "http://local-system/service/7784"
            ),
        ]

        conn.executemany("""
            INSERT INTO records (
                source,
                record_type,
                job_number,
                serial_number,
                summary,
                status,
                details,
                source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        conn.commit()

    conn.close()


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/search")
async def search_records(q: str = ""):
    query = (q or "").strip()
    if not query:
        return {"query": "", "results": []}

    search_term = f"%{query}%"

    conn = get_connection()
    rows = conn.execute("""
        SELECT
            source,
            record_type,
            job_number,
            serial_number,
            summary,
            status,
            details,
            source_url
        FROM records
        WHERE
            job_number LIKE ?
            OR serial_number LIKE ?
            OR summary LIKE ?
            OR source LIKE ?
            OR details LIKE ?
        ORDER BY source, record_type, job_number
    """, (search_term, search_term, search_term, search_term, search_term)).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "source": row["source"],
            "record_type": row["record_type"],
            "job_number": row["job_number"],
            "serial_number": row["serial_number"],
            "summary": row["summary"],
            "status": row["status"],
            "details": row["details"],
            "source_url": row["source_url"]
        })

    return {"query": query, "results": results}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
