import mysql.connector
def connect_db():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="daproject2")
    
    
    
    
def get_basic_info(cursor):
    """
    Retrieve summary inventory and supply chain metrics.

    Args:
        cursor (mysql.connector.cursor.MySQLCursorDict): Cursor object with dictionary=True.

    Returns:
        dict: Dictionary of metric labels and their values.
    """

    queries = {
        "Total Suppliers": "SELECT COUNT(*) AS count FROM suppliers",

        "Total Products": "SELECT COUNT(*) AS count FROM products",

        "Total Categories Dealing": "SELECT COUNT(DISTINCT category) AS count FROM products",

        "Total Sale Value (Last 3 Months)": """
            SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_sale
            FROM stock_entries se
            JOIN products p ON se.product_id = p.product_id
            WHERE se.change_type = 'Sale'
              AND se.entry_date >= (
                  SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Total Restock Value (Last 3 Months)": """
            SELECT ROUND(SUM(se.change_quantity * p.price), 2) AS total_restock
            FROM stock_entries se
            JOIN products p ON se.product_id = p.product_id
            WHERE se.change_type = 'Restock'
              AND se.entry_date >= (
                  SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Below Reorder & No Pending Reorders": """
            SELECT COUNT(*) AS below_reorder
            FROM products p
            WHERE p.stock_quantity < p.reorder_level
              AND p.product_id NOT IN (
                  SELECT DISTINCT product_id FROM reorders WHERE status = 'Pending')
        """
    }

    results = {}
    for label, query in queries.items():
        cursor.execute(query)
        row = cursor.fetchone()
        # Since row is a dictionary, extract the single value by getting the first value in dict.values()
        results[label] = list(row.values())[0]

    return results


def get_additonal_tables(cursor):
    queries = {
        "Suppliers Contact Details": "SELECT supplier_name, contact_name, email, phone FROM suppliers",

        "Products with Supplier and Stock": """
            SELECT 
                p.product_name,
                s.supplier_name,
                p.stock_quantity,
                p.reorder_level
            FROM products p
            JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_name ASC
        """,

        "Products Needing Reorder": """
            SELECT product_name, stock_quantity, reorder_level
            FROM products
            WHERE stock_quantity <= reorder_level
        """
    }

    tables = {}
    for label, query in queries.items():
        cursor.execute(query)
        tables[label] = cursor.fetchall()

    return tables



