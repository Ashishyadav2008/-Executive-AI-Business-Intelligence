import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def render_charts(df):
    """
    Auto-generate smart charts for ANY dataset
    """

    # Detect numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available for charts")
        return

    # Detect date/time column
    time_col = None
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                time_col = col
                break

    # -------- LINE CHARTS (Top 3 Variance) --------
    variance = df[numeric_cols].var().sort_values(ascending=False)
    top_numeric = variance.head(3).index.tolist()

    for col in top_numeric:
        fig, ax = plt.subplots()

        if time_col:
            ax.plot(df[time_col], df[col], marker="o")
            ax.set_xlabel(time_col)
        else:
            ax.plot(df[col], marker="o")
            ax.set_xlabel("Index")

        ax.set_ylabel(col)
        ax.set_title(f"{col} Trend")
        ax.grid(True)

        st.pyplot(fig)

    # -------- BAR CHART (Top Aggregated Column) --------
    best_col = top_numeric[0]

    fig, ax = plt.subplots()
    df[best_col].plot(kind="bar", ax=ax)
    ax.set_title(f"{best_col} Distribution")
    ax.set_xlabel("Index")
    ax.set_ylabel(best_col)

    st.pyplot(fig)
