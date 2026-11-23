import sqlite3
from pathlib import Path
from datetime import datetime
from .config import DB_NAME
from .security import hash_password

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / DB_NAME

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin','staff')),
            full_name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS suppliers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT DEFAULT '',
            email TEXT DEFAULT '',
            notes TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
            reorder_level INTEGER NOT NULL DEFAULT 5 CHECK(reorder_level >= 0),
            unit_price REAL NOT NULL DEFAULT 0 CHECK(unit_price >= 0),
            supplier_id INTEGER,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS stock_movements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER,
            movement_type TEXT NOT NULL CHECK(movement_type IN ('STOCK_IN','STOCK_OUT','ADJUSTMENT')),
            quantity INTEGER NOT NULL,
            note TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """)
        admin = con.execute("SELECT id FROM users WHERE username='admin'").fetchone()
        if not admin:
            con.execute(
                "INSERT INTO users(username,password_hash,role,full_name,created_at) VALUES(?,?,?,?,?)",
                ("admin", hash_password("Admin@123"), "admin", "System Administrator", now())
            )

def now():
    return datetime.now().isoformat(timespec="seconds")

def authenticate(username, password):
    from .security import verify_password
    with connect() as con:
        row = con.execute("SELECT * FROM users WHERE username=?", (username.strip(),)).fetchone()
        if row and verify_password(password, row["password_hash"]):
            return dict(row)
    return None

def create_user(username, password, full_name, role="staff"):
    if len(username.strip()) < 3 or len(password) < 8 or not full_name.strip():
        raise ValueError("Enter a name, username (3+ characters), and password (8+ characters).")
    with connect() as con:
        con.execute(
            "INSERT INTO users(username,password_hash,role,full_name,created_at) VALUES(?,?,?,?,?)",
            (username.strip(), hash_password(password), role, full_name.strip(), now())
        )

def list_users():
    with connect() as con:
        return con.execute("SELECT id,username,full_name,role,created_at FROM users ORDER BY id DESC").fetchall()

def add_supplier(name, contact="", email="", notes=""):
    with connect() as con:
        con.execute("INSERT INTO suppliers(name,contact,email,notes) VALUES(?,?,?,?)",
                    (name.strip(), contact.strip(), email.strip(), notes.strip()))

def suppliers():
    with connect() as con:
        return con.execute("SELECT * FROM suppliers ORDER BY name").fetchall()

def save_product(sku, name, category, quantity, reorder, price, supplier_id=None, product_id=None):
    values = (sku.strip(), name.strip(), category.strip(), int(quantity), int(reorder), float(price),
              int(supplier_id) if supplier_id else None, now())
    if not values[0] or not values[1] or not values[2]:
        raise ValueError("SKU, product name and category are required.")
    if values[3] < 0 or values[4] < 0 or values[5] < 0:
        raise ValueError("Quantity, reorder level and price cannot be negative.")
    with connect() as con:
        if product_id:
            con.execute("""UPDATE products SET sku=?,name=?,category=?,quantity=?,reorder_level=?,
                        unit_price=?,supplier_id=?,updated_at=? WHERE id=?""", values + (product_id,))
        else:
            con.execute("""INSERT INTO products(sku,name,category,quantity,reorder_level,unit_price,
                        supplier_id,updated_at) VALUES(?,?,?,?,?,?,?,?)""", values)

def products(search=""):
    with connect() as con:
        term = f"%{search.strip()}%"
        return con.execute("""SELECT p.*,s.name supplier_name FROM products p
            LEFT JOIN suppliers s ON p.supplier_id=s.id
            WHERE p.sku LIKE ? OR p.name LIKE ? OR p.category LIKE ?
            ORDER BY p.name""", (term,term,term)).fetchall()

def delete_product(product_id):
    with connect() as con:
        con.execute("DELETE FROM products WHERE id=?", (product_id,))

def record_movement(product_id, user_id, movement_type, quantity, note=""):
    quantity = int(quantity)
    if quantity <= 0:
        raise ValueError("Movement quantity must be greater than zero.")
    with connect() as con:
        product = con.execute("SELECT quantity FROM products WHERE id=?", (product_id,)).fetchone()
        if not product:
            raise ValueError("Product not found.")
        current = product["quantity"]
        if movement_type == "STOCK_OUT" and quantity > current:
            raise ValueError("Not enough stock available.")
        new_qty = current + quantity if movement_type == "STOCK_IN" else current - quantity
        con.execute("UPDATE products SET quantity=?,updated_at=? WHERE id=?", (new_qty,now(),product_id))
        con.execute("""INSERT INTO stock_movements(product_id,user_id,movement_type,quantity,note,created_at)
                       VALUES(?,?,?,?,?,?)""",
                    (product_id,user_id,movement_type,quantity,note.strip(),now()))

def dashboard_stats():
    with connect() as con:
        total = con.execute("SELECT COUNT(*) n FROM products").fetchone()["n"]
        units = con.execute("SELECT COALESCE(SUM(quantity),0) n FROM products").fetchone()["n"]
        low = con.execute("SELECT COUNT(*) n FROM products WHERE quantity<=reorder_level").fetchone()["n"]
        value = con.execute("SELECT COALESCE(SUM(quantity*unit_price),0) n FROM products").fetchone()["n"]
        recent = con.execute("""SELECT m.*,p.name product_name,u.username FROM stock_movements m
            JOIN products p ON p.id=m.product_id LEFT JOIN users u ON u.id=m.user_id
            ORDER BY m.id DESC LIMIT 8""").fetchall()
        return {"products":total,"units":units,"low_stock":low,"value":value,"recent":recent}

def movement_history():
    with connect() as con:
        return con.execute("""SELECT m.id,p.sku,p.name,u.username,m.movement_type,m.quantity,
            m.note,m.created_at FROM stock_movements m JOIN products p ON p.id=m.product_id
            LEFT JOIN users u ON u.id=m.user_id ORDER BY m.id DESC LIMIT 500""").fetchall()
