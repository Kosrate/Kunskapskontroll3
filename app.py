import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, inspect
import logging

# Set up logging
logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

# Skapa anslutning till SQLite-databasen
def connect_to_db():
    try:
        engine = create_engine("sqlite:///Köksglädje.db")
        return engine
    except Exception as e:
        st.error(f"Fel vid anslutning till databasen: {e}")
        logging.error(f"Database connection error: {e}")
        return None

# Funktion för att lista tabeller i databasen
def list_tables(engine):
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        st.error(f"Fel vid hämtning av tabellnamn: {e}")
        logging.error(f"Error fetching table names: {e}")
        return []

# Funktion för att läsa en specifik tabell
def fetch_table_data(engine, table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Fel vid hämtning av data från tabellen '{table_name}': {e}")
        logging.error(f"Error fetching data from table '{table_name}': {e}")
        return pd.DataFrame()

# Funktion för att uppdatera databasen med en ny DataFrame
def update_table_data(engine, table_name, df):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        st.success(f"Tabellen '{table_name}' har uppdaterats.")
    except Exception as e:
        st.error(f"Fel vid uppdatering av tabellen '{table_name}': {e}")
        logging.error(f"Error updating table '{table_name}': {e}")

# Start på Streamlit-appen
st.title("Köksglädje Databas Explorer")
st.write("Den här applikationen låter dig utforska och analysera data från flera tabeller i Köksglädjes SQLite-databas.")

# Anslut till databasen
engine = connect_to_db()
if engine:
    # Lista tillgängliga tabeller
    st.header("1. Välj en tabell att hämta")
    tables = list_tables(engine)

    if tables:
        selected_table = st.selectbox("Välj en tabell:", tables)

        # Hämta och visa data från den valda tabellen
        st.header("2. Data från vald tabell")
        df = fetch_table_data(engine, selected_table)
        if not df.empty:
            st.write(f"### Data från tabellen: {selected_table}")
            st.dataframe(df)

            # Filtrera data
            st.header("3. Filtrera data")
            filters = {}
            for col in df.columns:
                if df[col].dtype in [np.int64, np.float64]:
                    filters[col] = st.slider(f"Filtera {col} (intervall):", float(df[col].min()), float(df[col].max()), (float(df[col].min()), float(df[col].max())))
                elif df[col].dtype == object:
                    filters[col] = st.text_input(f"Filtera {col} (text):", "")

            filtered_df = df.copy()
            for col, val in filters.items():
                if isinstance(val, tuple):
                    filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
                elif isinstance(val, str) and val:
                    filtered_df = filtered_df[filtered_df[col].str.contains(val, na=False, case=False)]
            
            st.write("### Filtrerad data")
            st.dataframe(filtered_df)

            # Enkel analys och visualisering
            st.header("4. Enkel analys och visualisering")
            st.write("#### Beskrivande statistik:")
            st.write(filtered_df.describe())

            numeric_columns = filtered_df.select_dtypes(include=['number']).columns
            if not numeric_columns.empty:
                chart_type = st.selectbox("Välj typ av visualisering:", ["Bar Chart", "Line Chart", "Scatter Plot"])
                selected_column = st.selectbox("Välj en numerisk kolumn för visualisering:", numeric_columns)
                if chart_type == "Bar Chart":
                    st.bar_chart(filtered_df[selected_column])
                elif chart_type == "Line Chart":
                    st.line_chart(filtered_df[selected_column])
                elif chart_type == "Scatter Plot":
                    x_col = st.selectbox("Välj X-kolumn:", numeric_columns)
                    y_col = st.selectbox("Välj Y-kolumn:", numeric_columns)
                    st.write(filtered_df.plot.scatter(x=x_col, y=y_col))

            # Möjlighet att ladda upp uppdaterad data
            st.header("5. Uppdatera tabellen")
            uploaded_file = st.file_uploader("Ladda upp en CSV-fil för att ersätta tabellen", type="csv")
            if uploaded_file:
                new_df = pd.read_csv(uploaded_file)
                st.write("### Ny data:")
                st.dataframe(new_df)
                if st.button("Uppdatera tabellen"):
                    update_table_data(engine, selected_table, new_df)

        else:
            st.warning("Ingen data kunde hämtas från den valda tabellen.")
    else:
        st.warning("Inga tabeller hittades i databasen.")
else:
    st.error("Kunde inte ansluta till databasen.")
