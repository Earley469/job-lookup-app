# job-lookup-app

Local job/serial lookup app for internal network searching.

A small LAN web app: type a job number or serial number and get back matching
records from your internal systems, grouped in one place. This starter version
searches a local SQLite database seeded with sample records, and is structured
so real connectors (SQL Server, ERP/MES, file shares, SharePoint, APIs, etc.)
can be added later without redesigning the app.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open http://localhost:8000 in your browser.

## Try it

Search for any of the seeded sample values:

- `JOB-1001`
- `SN-ABC-2001`
- `JOB-2204`
- `SN-XYZ-9901`
- `JOB-3007`
- `SN-DEF-7784`

## API

- `GET /api/search?q=<job or serial number>` — search records by job number,
  serial number, summary, source, or details.
- `GET /api/health` — health check.

## Security notes

This app is intended to run on a trusted internal network only:

- Keep it off the public internet; restrict to LAN/VPN access.
- Add authentication before connecting it to real internal systems.
- Give it read-only access to source systems where possible.
- Store any real credentials in environment variables or a secrets manager,
  never in source code.
- Log searches for auditing, but never log passwords, tokens, or sensitive
  content.

## Next steps

- Replace the sample SQLite data with real connectors (SQL Server, MySQL,
  ERP/MES, file shares, SharePoint, REST APIs, CSV/Excel imports).
- Add authentication (local accounts or Active Directory/LDAP) and
  role-based access.
- Add document/PDF search and export-to-CSV.
- Add per-source dashboard tabs and audit logging.
