import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from database_utils import connect_to_db, list_tables, fetch_table_data, update_table_data, fetch_sales_data
from filtering import apply_filters
from data_visualization import visualize_data
from sales_analysis import analyze_sales

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

        if selected_table:
            # Hämta vald tabell
            st.header(f"Visar data för: {selected_table}")
            df = fetch_table_data(engine, selected_table)
            if not df.empty:
                st.dataframe(df)

                # Försäljningsdata (om relevant)
                if selected_table in ["Transactions", "TransactionDetails"]:
                    st.header("Försäljningsdata")
                    sales_data = fetch_sales_data(engine)
                    if not sales_data.empty:
                        st.dataframe(sales_data)
                        analyze_sales(sales_data)
                    else:
                        st.warning("Ingen försäljningsdata kunde hämtas.")

                # Filtrera data
                st.header("3. Filtrera data")
                filtered_df = apply_filters(df)
                st.write("### Filtrerad data")
                st.dataframe(filtered_df)

                # Enkel analys och visualisering
                st.header("4. Enkel analys och visualisering")
                visualize_data(filtered_df)

                # Möjlighet att ladda upp ny data
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
