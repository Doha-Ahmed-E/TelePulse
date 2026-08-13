# TelePulse Frontend

A lightweight vanilla HTML/CSS/JavaScript dashboard for the TelePulse FastAPI analytics service.

## Expected API

The dashboard expects:

- `GET /analytics/overview`
- `GET /analytics/cells`
- `GET /analytics/hourly`
- `GET /analytics/hourly?province=<name>`

By default the API is expected at `http://localhost:8000`.

## Run

From this directory:

```bash
python3 -m http.server 3000
```

Then open:

```text
http://localhost:3000
```

If the browser blocks requests because of CORS, add FastAPI CORS middleware to the API.
