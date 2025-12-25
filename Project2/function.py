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


def add_new_manual_id(cursor, db, p_name , p_category , p_price , p_stock , p_reorder, p_supplier):
    proc_call= "call AddNewProductManualID(%s, %s, %s ,%s ,%s, %s)"
    params= (p_name , p_category , p_price , p_stock , p_reorder, p_supplier)
    cursor.execute(proc_call, params)
    db.commit()
    

def get_categories(cursor):
    cursor.execute("select Distinct category  from products  order by category  asc")
    rows= cursor.fetchall()
    return [row["category"] for row in rows]


def get_suppliers(cursor):
    cursor.execute("select supplier_id , supplier_name from suppliers order by  supplier_name asc")
    return cursor.fetchall()


def get_product_histroy(cursor,product_id):
   query="select * from product_inventory_histroy where product_id=%s order by record_date Desc"
   cursor.execute(query,(product_id,))
   return cursor.fetchall()


def get_all_products(cursor):
    cursor.execute("select product_id, product_name from products order by product_name asc")
    return cursor.fetchall()


