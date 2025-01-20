import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def analyze_sales(df):
    if "TransactionDate" not in df.columns:
        st.error("Försäljningsdata saknar kolumnen 'TransactionDate'.")
        return
    st.header("Analys av försäljning")

    # Konvertera datum till datetime-format
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors="coerce")
    
    # Filtrera data
    st.sidebar.header("Filter")
    store_filter = st.sidebar.multiselect("Välj butiker:", df["StoreName"].unique())
    product_filter = st.sidebar.multiselect("Välj produkter:", df["ProductName"].unique())
    time_filter = st.sidebar.date_input("Välj tidsperiod:", [])

    if store_filter:
        df = df[df["StoreName"].isin(store_filter)]
    if product_filter:
        df = df[df["ProductName"].isin(product_filter)]
    if time_filter and len(time_filter) == 2:
        df = df[(df["TransactionDate"] >= time_filter[0]) & (df["TransactionDate"] <= time_filter[1])]

    # Försäljning per butik
    st.subheader("Försäljning per butik")
    sales_by_store = df.groupby("StoreName")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_by_store.set_index("StoreName"))

    # Försäljning per produkt
    st.subheader("Försäljning per produkt")
    sales_by_product = df.groupby("ProductName")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_by_product.set_index("ProductName"))

    # Försäljning över tid
    st.subheader("Försäljning över tid")
    df["YearMonth"] = df["TransactionDate"].dt.to_period("M")
    sales_over_time = df.groupby("YearMonth")["TotalSales"].sum().reset_index()
    sales_over_time["YearMonth"] = sales_over_time["YearMonth"].astype(str)
    plt.figure(figsize=(10, 5))
    plt.plot(sales_over_time["YearMonth"], sales_over_time["TotalSales"], marker="o")
    plt.title("Försäljningstrender över tid")
    plt.xlabel("Månad")
    plt.ylabel("Total försäljning")
    plt.xticks(rotation=45)
    st.pyplot(plt)

