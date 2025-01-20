import streamlit as st
from database_utils import connect_to_db, list_tables, fetch_table_data, update_table_data
from filtering import apply_filters
from data_visualization import visualize_data
from database_utils import fetch_sales_data
from sales_analysis import analyze_sales
import sys
print(sys.path)
print(analyze_sales)

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
            
            # Hämta försäljningsdata
            st.header("Försäljningsdata")
            sales_data = fetch_sales_data(engine)
            if not sales_data.empty:
                st.write("### Försäljningsdata")
                st.dataframe(sales_data)
                
                # Analysera försäljningsdata
            analyze_sales(sales_data)
        else:
            st.warning("Ingen data kunde hämtas från den valda tabellen.")

            # Filtrera data
            st.header("3. Filtrera data")
            filtered_df = apply_filters(df)
            st.write("### Filtrerad data")
            st.dataframe(filtered_df)

            # Enkel analys och visualisering
            st.header("4. Enkel analys och visualisering")
            st.write("#### Beskrivande statistik:")
            st.write(filtered_df.describe())
            visualize_data(filtered_df)

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
