import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect

# Skapa anslutning till SQLite-databasen
def connect_to_db():
    try:
        engine = create_engine("sqlite:///Köksglädje.db")
        return engine
    except Exception as e:
        st.error(f"Fel vid anslutning till databasen: {e}")
        return None

# Funktion för att lista tabeller i databasen
def list_tables(engine):
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        st.error(f"Fel vid hämtning av tabellnamn: {e}")
        return []

# Funktion för att läsa en specifik tabell
def fetch_table_data(engine, table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Fel vid hämtning av data från tabellen '{table_name}': {e}")
        return pd.DataFrame()

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

            # Enkel analys och visualisering
            st.header("3. Enkel analys och visualisering")
            st.write("#### Beskrivande statistik:")
            st.write(df.describe())

            # Visualisering av en numerisk kolumn (om det finns)
            numeric_columns = df.select_dtypes(include=['number']).columns
            if not numeric_columns.empty:
                selected_column = st.selectbox("Välj en numerisk kolumn för visualisering:", numeric_columns)
                st.bar_chart(df[selected_column])
            else:
                st.warning("Inga numeriska kolumner hittades för visualisering.")
        else:
            st.warning("Ingen data kunde hämtas från den valda tabellen.")
    else:
        st.warning("Inga tabeller hittades i databasen.")
