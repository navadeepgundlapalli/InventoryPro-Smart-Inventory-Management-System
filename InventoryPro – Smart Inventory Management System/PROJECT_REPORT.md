# INVENTORYPRO
## Smart Inventory Management System
### Python GUI-Based Semester Capstone Project

**Submitted by:** [Student Name]  
**Programme:** B.Tech — Computer Science and Engineering  
**Semester:** [Semester]  
**College:** [College Name]  
**Academic Year:** 2026–2027

---

## Certificate
This is to certify that the project titled **“InventoryPro – Smart Inventory Management System”** is a bona fide academic project developed by [Student Name] as part of the semester project requirements. The work was completed under the guidance of [Faculty Name].

## Declaration
I declare that this project is my academic work. External libraries, documentation and learning resources used during development have been acknowledged. I understand the design and implementation and will explain the modules during evaluation.

## Acknowledgement
I express my sincere gratitude to my faculty guide, department and institution for their guidance and support. I also acknowledge the Python and SQLite documentation, which helped inform the implementation.

## Abstract
InventoryPro is a desktop-based inventory management application developed using Python and SQLite. It provides a graphical interface for managing products, suppliers, stock movements and basic inventory reports. Authentication separates administrator and staff access. The dashboard summarizes product count, total units, low-stock items and estimated inventory value. Product records can be searched and maintained, while stock-in and stock-out transactions update quantities and create a movement history. CSV exports support further analysis in spreadsheet software. The project demonstrates GUI development, relational database design, input validation, password hashing, role-based access and modular programming.

**Keywords:** Python, Tkinter, SQLite, inventory, GUI, authentication, stock management.

## 1. Introduction
Small shops, laboratories and departments often track inventory using notebooks or disconnected spreadsheets. Such methods can make it difficult to identify low-stock items, trace stock changes and prepare consistent reports. InventoryPro provides a centralized desktop prototype for these tasks. It is designed as an educational project and can be extended for a real organization after additional security, backup and testing work.

## 2. Problem Statement
Manual inventory tracking can lead to duplicate records, inaccurate stock totals, delayed replenishment and limited visibility into stock movement. The project aims to create a simple GUI-based system that stores product and supplier information, records stock transactions and presents key inventory indicators.

## 3. Objectives
1. Build an intuitive Python desktop GUI.
2. Provide login and staff registration.
3. Separate administrator and staff capabilities.
4. Maintain product and supplier records.
5. Record stock-in and stock-out operations.
6. Prevent stock-out transactions exceeding available quantity.
7. Display inventory summaries and low-stock counts.
8. Export inventory and movement data to CSV.

## 4. Scope
The prototype is intended for a small inventory desk, college laboratory or small retail store. It supports one local SQLite database on the computer where it runs. It does not currently provide cloud synchronization, barcode scanning, purchase-order workflows, multi-branch stock or tax invoicing.

## 5. Technology Stack
| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| Tkinter and ttk | Desktop graphical interface |
| SQLite | Local relational database |
| hashlib / secrets | Salted password hashing |
| csv | Report export |
| Git (recommended) | Version control |

## 6. System Requirements
**Hardware:** Dual-core processor or better, 4 GB RAM recommended, 200 MB free disk space, keyboard and display.  
**Software:** Windows, Linux or macOS with Python 3.10+ and Tkinter support.

## 7. System Design
### 7.1 Architecture
The application follows a simple three-layer structure:
- Presentation layer: login window and dashboard screens in `auth_ui.py` and `ui.py`.
- Logic/data-access layer: validation and inventory operations in `database.py`.
- Storage layer: SQLite tables in `inventorypro.db`.

### 7.2 Database Tables
**users:** id (PK), username (unique), password_hash, role, full_name, created_at.  
**suppliers:** id (PK), name, contact, email, notes.  
**products:** id (PK), sku (unique), name, category, quantity, reorder_level, unit_price, supplier_id (FK), updated_at.  
**stock_movements:** id (PK), product_id (FK), user_id (FK), movement_type, quantity, note, created_at.

### 7.3 Relationships
- One supplier can be associated with many products.
- One product can have many stock movement records.
- One user can record many stock movements.
- A product may have no supplier; deleting a supplier sets the product's supplier reference to NULL.

## 8. Module Description
**Authentication:** verifies username and password against salted PBKDF2 password hashes. Staff can register their own staff account.  
**Role-based access:** admin can access user administration and product deletion; staff cannot.  
**Dashboard:** displays product types, total units, low-stock item count, inventory value and recent stock activity.  
**Product catalogue:** add, edit (double-click), search and admin-delete product records.  
**Supplier management:** add and list supplier contacts.  
**Stock movement:** record incoming and outgoing stock; the system blocks outgoing quantities greater than available stock.  
**Reports:** export product inventory and stock movement history to CSV.

## 9. Implementation
Run the application with `python main.py`. On first launch the database and starter admin account are created automatically. The starter credentials are `admin` / `Admin@123`; change them before real deployment. Product quantities are stored as integers. Monetary values are stored as floating-point values for this academic prototype; a production financial system should use integer minor units or a decimal-safe approach.

## 10. Testing
| Test case | Expected result |
|---|---|
| Valid admin login | Dashboard opens |
| Invalid password | Error message |
| Register staff with short password | Validation error |
| Add product with unique SKU | Product saved |
| Add duplicate SKU | Database rejects duplicate |
| Stock-in transaction | Quantity increases |
| Stock-out transaction within stock | Quantity decreases |
| Stock-out greater than stock | Transaction rejected |
| Search by product name | Matching products shown |
| Staff login | User administration hidden |
| CSV export | File saved with headings and records |

## 11. Security and Validation
Passwords are not stored as plain text. A random salt and PBKDF2-HMAC-SHA256 are used to derive password hashes. SQL statements use parameterized queries. Database foreign keys and quantity constraints protect basic data integrity. This is an academic prototype: it does not yet include account lockout, password reset, encrypted database storage or a full admin password-change workflow.

## 12. Results
The implemented prototype provides a single interface for product, supplier and stock movement tasks. The dashboard presents high-level inventory indicators. The movement table supports traceability of stock changes, and CSV exports allow the records to be reviewed externally. Actual results should be captured as screenshots after running the project on the student's computer.

## 13. Limitations
The application is designed for local single-computer use. It has no network synchronization, barcode scanner integration, automated email alerts, invoice generation or role customization. The starter admin password must be changed before any real use.

## 14. Future Enhancements
- Admin password-change and password-reset workflow.
- Automatic low-stock notifications.
- Barcode/QR code scanning.
- Purchase orders and sales invoices.
- Interactive charts and date-filtered analytics.
- Automated unit and integration tests.
- Database backup and restore.
- Multi-user network deployment with a server database.

## 15. Conclusion
InventoryPro demonstrates how Python GUI programming and SQLite can be combined to create a modular inventory management prototype. It covers authentication, role separation, product and supplier records, stock transactions, validation and reporting. The project provides a foundation for further work in database systems, software engineering and business process automation.

## References
1. Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
2. Python Software Foundation. *tkinter — Python interface to Tcl/Tk*. https://docs.python.org/3/library/tkinter.html
3. SQLite Consortium. *SQLite Documentation*. https://www.sqlite.org/docs.html
4. Python Software Foundation. *sqlite3 — DB-API 2.0 interface for SQLite databases*. https://docs.python.org/3/library/sqlite3.html
5. Python Software Foundation. *hashlib — Secure hashes and message digests*. https://docs.python.org/3/library/hashlib.html
6. Python Software Foundation. *secrets — Generate secure random numbers*. https://docs.python.org/3/library/secrets.html
7. Python Software Foundation. *csv — CSV File Reading and Writing*. https://docs.python.org/3/library/csv.html
8. OWASP Foundation. *Password Storage Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
9. Elmasri, R. and Navathe, S. B. *Fundamentals of Database Systems*. Pearson.
10. Sommerville, I. *Software Engineering*. Pearson.

## Appendix A — Run Instructions
1. Install Python 3.10 or later.
2. Extract the project ZIP.
3. Open a terminal in the extracted folder.
4. Execute `python main.py`.
5. Sign in with the starter admin credentials and create a staff account for role testing.

## Appendix B — Screenshot Checklist
Insert original screenshots of: login screen, admin dashboard, product catalogue, add-product form, supplier screen, stock movement screen, low-stock dashboard state, CSV report opened in spreadsheet software, staff dashboard. Add figure numbers and brief captions.
