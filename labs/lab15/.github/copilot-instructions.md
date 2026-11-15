## Purpose
Provide concise, actionable guidance to AI coding agents working on this small Flask-based report app.

## Quick summary (what this repo does)
- A tiny Flask app with a single route (`/`) that renders a customer invoice report based on POSTed `last_name`.
- Data is read from a local SQLite DB (`retail_app.db`) using `pandas.read_sql_query`, then converted to HTML (`DataFrame.to_html`) and injected into the template.

## Key files
- `create_report.py` — Flask app. Endpoint: `customer_invoice_report()` handles GET and POST. Uses:
  - `db_file = Path(__file__).resolve().parent.parent / "retail_app.db"` (DB expected two levels up from this file)
  - Parameterized SQL query with `?` and `params=(last_name,)`
  - `pandas.read_sql_query` to build a DataFrame and `df.to_html(index=False)` for the template
- `create_report.html` — template with a POST form field `last_name` and conditional rendering of `customer_invoice_info` (marked safe).

## How to run (discovered from code)
1. Create and activate a Python venv (recommended).
   - python3 -m venv .venv
   - source .venv/bin/activate
2. Install minimal deps: Flask and pandas
   - pip install flask pandas
3. Ensure the SQLite DB is present at the expected location: repo_root/../retail_app.db (the code resolves two levels up from `create_report.py`).
   - Running from `/Users/arzumalkoc/Desktop/sql/lab15`, the DB should be at `/Users/arzumalkoc/Desktop/sql/retail_app.db`.
4. Start the app:
   - python3 create_report.py
   - Server starts in debug mode on 127.0.0.1:5000 by default.
5. Use the web form: POST a `last_name` value to see the returned HTML table.

## Patterns & conventions to follow (derived from code)
- Use parameterized queries (`?`) with `sqlite3` to avoid SQL injection (this repo already follows that).
- Data access flows: SQL -> pandas.DataFrame -> DataFrame.to_html -> Jinja template (safe-escaped via `| safe`).
- Templates are rendered via Flask `render_template('create_report.html')`. Ensure templates live in Flask's `templates/` dir (or update `Flask(__name__, template_folder=...)`) — the repo contains `create_report.html` at the repo root; when running, ensure the template is reachable by Flask.

## Debugging tips (project-specific)
- If the page shows a template error, confirm `create_report.html` is in the `templates/` folder or change Flask app instantiation accordingly.
- If no rows are returned, the code returns the string `No information to report.` — check the DB path and confirm `customer` / `invoice` tables exist.
- Quick DB check: `sqlite3 /path/to/retail_app.db` then run the query in the code to verify results.

## Small safety notes
- The app calls `customer_invoice_info = df.to_html(...)` and outputs it with `| safe` in Jinja. This is acceptable for this internal reporting tool but be mindful of HTML injection if upstream data is untrusted.

## Examples to reference in edits/PRs
- When adding features, follow the same data-flow: perform SQL via parameterized query, return a DataFrame, and use `to_html` for simple HTML embedding.
- Example SQL pattern (from `create_report.py`):
```
query = """
SELECT customer.customer_id, customer.customer_last_name, invoice.invoice_total
FROM customer
INNER JOIN invoice ON customer.customer_id = invoice.customer_id
WHERE customer.customer_last_name = ?
"""
df = pd.read_sql_query(query, conn, params=(last_name,))
```

## When merging/adding copilot instructions
- If a `.github/copilot-instructions.md` already exists in future, merge by:
  1. Preserving run/debug steps and DB path notes.
  2. Updating any new dependency commands (requirements or docker changes).

## Ask the user
- Is the SQLite DB intentionally placed two levels up from `create_report.py`, or should the app be updated to look for `templates/` and `retail_app.db` relative to the project root? Tell me which layout you want and I'll update the app or instructions.

----
If you want, I can also add a minimal `requirements.txt`, move the template into a `templates/` folder, and add a short `README.md` with run steps. Which do you prefer?
