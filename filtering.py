import streamlit as st
import numpy as np

def apply_filters(df):
    filters = {}

    for col in df.columns:
        if df[col].dtype in [np.int64, np.float64]:
            min_val, max_val = float(df[col].min()), float(df[col].max())
            if min_val < max_val:
                filters[col] = st.slider(
                    f"Filtera {col} (intervall):",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                )
            else:
                st.info(f"Kolumnen '{col}' har ett konstant värde: {min_val}")
        elif df[col].dtype == object:
            filters[col] = st.text_input(f"Filtera {col} (text):", "")

    filtered_df = df.copy()
    for col, val in filters.items():
        if isinstance(val, tuple):  # Numeric range filter
            filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
        elif isinstance(val, str) and val:  # Text filter
            filtered_df = filtered_df[filtered_df[col].str.contains(val, na=False, case=False)]

    return filtered_df
