import streamlit as st

def visualize_data(df):
    numeric_columns = df.select_dtypes(include=['number']).columns
    if not numeric_columns.empty:
        chart_type = st.selectbox("Välj typ av visualisering:", ["Bar Chart", "Line Chart", "Scatter Plot"])
        selected_column = st.selectbox("Välj en numerisk kolumn för visualisering:", numeric_columns)
        if chart_type == "Bar Chart":
            st.bar_chart(df[selected_column])
        elif chart_type == "Line Chart":
            st.line_chart(df[selected_column])
        elif chart_type == "Scatter Plot":
            x_col = st.selectbox("Välj X-kolumn:", numeric_columns)
            y_col = st.selectbox("Välj Y-kolumn:", numeric_columns)
            st.write(df.plot.scatter(x=x_col, y=y_col))
