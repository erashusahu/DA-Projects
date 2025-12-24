import streamlit as lt
import pandas as pd
from function import connect_db,get_basic_info

#sidebar
lt.sidebar.title("Inventory Mangement System")
option=lt.sidebar.radio("Select View",options=["Basic Information","Operational Tasks"])


#main space
lt.title("Inventory & Supply Chain Dashboard")
db=connect_db()
cursor=db.cursor(dictionary=True)

#-------------------this is basic information page---------------

if option == "Basic Information":
    lt.header("Basic Information")
    info = get_basic_info(cursor)   # example: {"total_suppliers": 10, "total_products": 50, ...}

    cols = lt.columns(3)
    keys = list(info.keys())

    for i in range(min(3, len(keys))):
        k = keys[i]
        cols[i].metric(label=k.replace("_", " ").title(), value=info[k])