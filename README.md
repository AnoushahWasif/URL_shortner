# URL shortener

A small URL shortener built with Flask and SQLite, from 2024. Paste a long URL, get a short code, and visiting the short link redirects to the original.

## Run it

```bash
python -m venv venv
venv\Scripts\activate        # on macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000. The SQLite database (`database.db`) is created on first run.

## Limitations

- `app.secret_key` is a hard-coded placeholder. It should come from an environment variable.
- Short codes are random with no collision check, and long URLs aren't validated.
- No tests.
