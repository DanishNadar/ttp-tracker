# TTP Outreach Stack (Tracker + DB + Email Sender)

This bundle adds:
- **Open tracking** (pixel + click redirect) -> SQLite DB
- **Scenario-based outreach** using your scanner output (`ttpResults.xlsx`)
- **Excel status updates** (`Email Sent`, `Email Open`, etc.)

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure
```bash
cp .env.example .env
# edit .env
```

Minimum required:
- `PUBLIC_BASE_URL` (public HTTPS URL where tracker runs)
- `TRACK_DB_PATH`
- SMTP: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SENDER_EMAIL`

## Run your scanner
Your existing scanner writes `ttpResults.xlsx`:
```bash
python /mnt/data/ttpDomainScanner.py
```

## Run tracker (dev)
```bash
python tracker_app.py
```
Production: host behind HTTPS (reverse proxy or platform deploy).

## Send outreach
```bash
python sender_outreach.py
```
Dry run:
```bash
DRY_RUN=true python sender_outreach.py
```

## Sync opens back to Excel
Run periodically (cron every 10–30 minutes):
```bash
python sync_opens.py
```

## Important note about DMARC weak vs missing
Your scanner logs DMARC weak as ISSUE, but the Excel currently stores only a boolean DMARC value.
If you want Scenario 1 to trigger perfectly, add a `DMARC Status` column to the sheet and write the string status.
