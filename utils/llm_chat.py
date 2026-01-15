import os
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _build_data_context(df: pd.DataFrame) -> str:
    """
    Create an intelligent summary of ANY dataset
    """

    summary = []

    summary.append(f"Total rows: {len(df)}")
    summary.append(f"Total columns: {len(df.columns)}")
    summary.append(f"Columns: {list(df.columns)}\n")

    # -------- NUMERIC SUMMARY --------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        summary.append("Numeric Columns Summary:")
        for col in numeric_cols:
            summary.append(
                f"- {col}: sum={df[col].sum():.2f}, "
                f"mean={df[col].mean():.2f}, "
                f"min={df[col].min():.2f}, "
                f"max={df[col].max():.2f}"
            )

        if len(numeric_cols) > 1:
            summary.append("\nCorrelations:")
            summary.append(df[numeric_cols].corr().round(2).to_string())

    # -------- CATEGORICAL SUMMARY --------
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    if categorical_cols:
        summary.append("\nCategorical Columns Summary:")
        for col in categorical_cols:
            top_val = df[col].mode()[0] if not df[col].mode().empty else "N/A"
            summary.append(f"- {col}: most frequent = {top_val}")

    # -------- DATE RANGE --------
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                summary.append(
                    f"\nTime Range ({col}): "
                    f"{df[col].min()} → {df[col].max()}"
                )
                break

    return "\n".join(summary)


def ask_llm(query: str, df: pd.DataFrame) -> str:
    """
    Ask AI with full business + data awareness
    """

    data_context = _build_data_context(df)

    prompt = f"""
You are a senior business analyst and data scientist.

Dataset context:
{data_context}

User question:
{query}

Instructions:
- Give clear, actionable business insights
- Mention trends, anomalies, risks if visible
- If prediction or decision is possible, explain it
- Avoid technical jargon unless necessary
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
