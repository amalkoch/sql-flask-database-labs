# 07 · SQL & Database Labs

Course labs that build a small **retail app database** (SQLite) and Flask web pages on top of it, plus a final project.

**Source:** `~/Desktop/sql/`, `~/Downloads/FINAL/`
**Stack:** SQL, SQLite, Python 3, Flask, pandas, matplotlib, HTML/CSS

## `labs/`
| Lab | Content |
|---|---|
| `lab08.html`, `lab09*.html` | SQL query results |
| `frontend/` (lab10) | HTML/CSS pages |
| `lab11-python/` | Python basics (p1–p7) |
| `lab12q1.py` | Tuples and indexing |
| `labb14/` | Flask CRUD app: add/get employee, customer, manager |
| `lab15/` | Report generation (`create_report.py`) |
| `lab16/` | matplotlib charts served through Flask templates |
| `lab17/`, `lab18/` | Static CSS and a Flask template |
| `lab19/` | CSV import and queries (`import_csv.py`, `queries.py`) |
| `lab20/` | Figures and practice problems |
| `*.csv`, `retail_app.db` | Seed data (customer, employee, invoice, manager, product, seller) |


## `final-project/`
`customer_info_app.py`: a Flask app that reads `retail_app.db` and renders `templates/customers.html` and `templates/customer_age_chart.html`. Also includes the `tutors_*.db` databases.

## Run
```bash
pip install flask pandas matplotlib
cd labs/labb14 && python add_employee.py   # then open http://127.0.0.1:5000
```

## Status (checked 2026-11-07)
**🟢 Complete**, except lab17. Every Flask page was tested by loading it *and* submitting its form (the add forms were tested on a throwaway copy of the database).
- ✅ All 13 pages work: labb14 add_customer, add_employee, get_employee, get_employee_by_last_name, get_manager · lab15 create_report · lab16 gender, inventory, units-sold and degree charts, create_plot · lab18 · **final-project** `/customers` and `/customer_age_chart`.
- 🔧 **Fixed in this pass** (most were SQL using column names that don't exist in `retail_app.db`):
  - `get_manager`: wrote the missing `templates/get_manager.html`, and `employee_first_name` → `first_name`.
  - `create_degree_line_chart`: wrote the missing template, and queried `employee.degree` instead of a non-existent `employee_degree` table. Each request now draws a fresh chart.
  - `get_employee_by_last_name`: `employee_last_name` → `last_name`.
  - `lab15/create_report`: `customer_last_name` / `invoice_total` → `last_name` / `total`.
  - `create_product_inventory_bar_chart`: `product_code, units_in_stock` → `product_id, inventory`.
  - `create_units_sold_line_chart`: the non-existent `order_items` table → `SUM(units)` from `invoice`.
  - `add_customer`: the form's field names now match the script, and the insert uses the table's real columns. Gender is saved as M/F.
  - `add_employee`: **finished it.** It used to reply "Form received!" without saving; now it inserts the employee the same way add_customer does.
- 🔧 **Earlier pass:** final-project HTML moved into `templates/` and a copy of `retail_app.db` added. lab15 HTML moved into `templates/`. lab19 `retail_app_db` renamed to `retail_app.db`. Empty `lab05.sql`, `lab14` and `lab14.py` removed.
- ❌ **lab17** has only a CSS file (`static/blue_color.css`) and no app or page.
- ℹ️ Some lab16/lab19/lab20 scripts open `"retail_app.db"` relative to the current folder, so run them from inside their own lab folder. `final-project/tutors_*.db` isn't used by `customer_info_app.py`.
