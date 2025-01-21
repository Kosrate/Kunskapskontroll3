import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def visualize_data(df):
    """
    Visualisera data med olika grafer baserat på användarens val.
    """
    # Kontrollera numeriska kolumner
    numeric_columns = df.select_dtypes(include=['number']).columns
    if numeric_columns.empty:
        st.warning("Tabellen innehåller inga numeriska kolumner att visualisera.")
        return

    # Användaren väljer typ av visualisering
    chart_type = st.selectbox("Välj typ av visualisering:", ["Bar Chart", "Line Chart", "Scatter Plot"])

    if chart_type == "Bar Chart":
        selected_column = st.selectbox("Välj en numerisk kolumn för visualisering:", numeric_columns)
        st.bar_chart(df[selected_column])

    elif chart_type == "Line Chart":
        selected_column = st.selectbox("Välj en numerisk kolumn för visualisering:", numeric_columns)
        st.line_chart(df[selected_column])

    elif chart_type == "Scatter Plot":
        if len(numeric_columns) < 2:
            st.warning("Tabellen innehåller inte tillräckligt med numeriska kolumner för att skapa en scatter plot.")
            return

        # Välj X- och Y-axlar
        x_col = st.selectbox("Välj X-kolumn:", numeric_columns, key="scatter_x")
        y_col = st.selectbox("Välj Y-kolumn:", numeric_columns, key="scatter_y")

        # Kontrollera att data finns
        valid_data = df[[x_col, y_col]].dropna()
        if valid_data.empty:
            st.warning("Ingen giltig data för scatter plot.")
            return

        # Rita scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(valid_data[x_col], valid_data[y_col], alpha=0.7, s=50)
        plt.title(f"Scatter Plot mellan {x_col} och {y_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        st.pyplot(plt)
