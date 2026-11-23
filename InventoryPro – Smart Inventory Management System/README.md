# InventoryPro — Python Semester Capstone

A desktop inventory management application built with Python, Tkinter/ttk and SQLite. It includes authentication, admin/staff roles, product catalogue, suppliers, stock-in/stock-out transactions, dashboard metrics, movement history and CSV exports.

## Run
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. (Optional) create a virtual environment.
4. Run `python main.py`.

No third-party package is required: the interface uses Python's built-in Tkinter and SQLite modules. `requirements.txt` is retained for optional future UI enhancements.

## First login
- Username: `admin`
- Password: `Admin@123`

Change the starter password before using the project with real business data. Create staff accounts from **User Accounts** (admin) or **Create staff account** on the login screen.

## Roles
- Admin: dashboard, products, delete products, stock movements, suppliers, reports, user account listing and staff account creation.
- Staff: dashboard, products, stock movements, suppliers, reports. Staff cannot access user administration or delete products.

## Main modules
- `inventorypro/database.py`: schema, database access, validation, business operations.
- `inventorypro/security.py`: salted PBKDF2-HMAC-SHA256 password hashing.
- `inventorypro/auth_ui.py`: login and staff registration.
- `inventorypro/ui.py`: dashboard and application screens.
- `main.py`: application entry point.

## Database
SQLite database `inventorypro.db` is created automatically beside `main.py`. Tables: users, suppliers, products and stock_movements. Foreign keys are enabled on each connection.

## Test checklist
1. Sign in with the starter admin account.
2. Add a supplier.
3. Add a product with an opening quantity.
4. Record STOCK_IN and STOCK_OUT movements.
5. Attempt a stock-out larger than available quantity; it should be rejected.
6. Search the product catalogue.
7. Export inventory and movement CSV files.
8. Create a staff account, log out and sign in as staff.
9. Confirm staff does not see the User Accounts screen or Delete Selected action.

## Limitations and future improvements
This is an academic prototype. Before production use, add password reset, admin password-change screen, backups, audit-log protection, stronger deployment controls, automated tests, pagination and a more comprehensive role/permission editor. The starter admin password is intentionally documented for first-run classroom demonstration and must be changed before any real deployment.
