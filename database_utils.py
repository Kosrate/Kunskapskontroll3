import pandas as pd
from sqlalchemy import create_engine, inspect
import logging
import streamlit as st

logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

def connect_to_db():
    try:
        engine = create_engine("sqlite:///Köksglädje.db")
        return engine
    except Exception as e:
        st.error(f"Fel vid anslutning till databasen: {e}")
        logging.error(f"Database connection error: {e}")
        return None

def list_tables(engine):
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        st.error(f"Fel vid hämtning av tabellnamn: {e}")
        logging.error(f"Error fetching table names: {e}")
        return []

def fetch_table_data(engine, table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Fel vid hämtning av data från tabellen '{table_name}': {e}")
        logging.error(f"Error fetching data from table '{table_name}': {e}")
        return pd.DataFrame()

def update_table_data(engine, table_name, df):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        st.success(f"Tabellen '{table_name}' har uppdaterats.")
    except Exception as e:
        st.error(f"Fel vid uppdatering av tabellen '{table_name}': {e}")
        logging.error(f"Error updating table '{table_name}': {e}")

def fetch_sales_data(engine):
    query = """
    SELECT 
        t.TransactionDate,
        s.StoreName,
        p.ProductName,
        td.Quantity,
        td.Price,
        (td.Quantity * td.Price) AS TotalSales
    FROM Transactions t
    JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
    JOIN Products p ON td.ProductID = p.ProductID
    JOIN Stores s ON t.StoreID = s.StoreID;
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        print(f"Error fetching sales data: {e}")
        return pd.DataFrame()