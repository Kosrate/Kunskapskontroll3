import streamlit as st
import numpy as np

def apply_filters(df):
    """
    Filtrera en DataFrame dynamiskt baserat på kolumntyp (numeriska, kategoriska, text).
    Inkluderar en reset-knapp och tomma filter som standard.
    """
    st.sidebar.header("Filter")

    # Reset-knapp
    reset = st.sidebar.button("Återställ filter")
    filters = {}

    # Kategoriska kolumner
    categorical_columns = [col for col in df.columns if df[col].nunique() < 20 and df[col].dtype == "object"]
    for col in categorical_columns:
        unique_values = df[col].dropna().unique()
        default_value = [] if reset or not st.session_state.get(f"{col}_filter_set", False) else st.session_state.get(f"{col}_filter", [])
        selected_values = st.sidebar.multiselect(f"Filtera {col}:", options=unique_values, default=default_value)
        filters[col] = selected_values
        st.session_state[f"{col}_filter"] = selected_values
        st.session_state[f"{col}_filter_set"] = True

    # Numeriska kolumner
    numeric_columns = df.select_dtypes(include=["number"]).columns
    for col in numeric_columns:
        min_val, max_val = float(df[col].min()), float(df[col].max())
        if min_val < max_val:  # Skapa slider endast om intervallet är giltigt
            filters[col] = st.sidebar.slider(
                f"Filtrera {col} (intervall):",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )
        else:  # Visa ett meddelande om intervallet är konstant
            filters[col] = (min_val, max_val)  # Använd samma värde för filtrering, men visa ingen slider
            st.sidebar.info(f"Kolumnen '{col}' har ett konstant värde: {min_val}")

    # Textbaserade kolumner
    text_columns = [col for col in df.columns if df[col].dtype == "object" and col not in categorical_columns]
    for col in text_columns:
        default_value = "" if reset or not st.session_state.get(f"{col}_filter_set", False) else st.session_state.get(f"{col}_filter", "")
        entered_text = st.sidebar.text_input(f"Sök i {col}:", value=default_value)
        filters[col] = entered_text
        st.session_state[f"{col}_filter"] = entered_text
        st.session_state[f"{col}_filter_set"] = True

    # Applicera filter
    filtered_df = df.copy()
    for col, val in filters.items():
        if col in categorical_columns:  # Filter för kategoriska kolumner
            if val:  # Endast filtrera om användaren gjort ett val
                filtered_df = filtered_df[filtered_df[col].isin(val)]
        elif col in numeric_columns:  # Filter för numeriska kolumner
            if isinstance(val, tuple):  # Endast filtrera om det är ett intervall
                filtered_df = filtered_df[(filtered_df[col] >= val[0]) & (filtered_df[col] <= val[1])]
        elif col in text_columns:  # Filter för textbaserade kolumner
            if val:  # Endast filtrera om användaren angett en sökterm
                filtered_df = filtered_df[filtered_df[col].str.contains(val, case=False, na=False)]

    return filtered_df
