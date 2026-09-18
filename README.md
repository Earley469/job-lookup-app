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

## Network folder search

In addition to the sample database, the app searches network folders configured
in `config.json`:

```json
{
  "network_search_paths": [
    "I:\\Eng. Jobs",
    "G:\\Manuals",
    "I:\\Mechanical"
  ]
}
```

A search matches any folder or file whose *name* contains the query text
(case-insensitive), up to 6 levels deep under each configured path. It does not
search inside file contents (e.g. text inside a PDF). If a path isn't reachable
(e.g. a network drive isn't currently mapped), the app skips it and shows a
warning in the UI rather than failing the whole search.

Edit `network_search_paths` in `config.json` to match the paths on your network
— no code changes needed. Add or remove paths as needed.

## API

- `GET /api/search?q=<job, serial, or assembly number>` — searches the sample
  database and the configured network folders, and returns combined results.
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
  ERP/MES, SharePoint, REST APIs, CSV/Excel imports).
- Add a SolidWorks PDM connector (via its SQL Server database, once the
  instance name is known) instead of just browsing its vault as a file share.
- Add authentication (local accounts or Active Directory/LDAP) and
  role-based access.
- Search inside file contents (PDF text, Excel cell values), not just names.
- Add export-to-CSV.
- Add per-source dashboard tabs and audit logging.
- Run on an always-on server/PC (not a laptop) once this needs to be shared
  with coworkers, not just used locally.
