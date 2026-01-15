from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import matplotlib.pyplot as plt
import pandas as pd
import os


def generate_report(df, predictions=None):
    """
    Generate Executive AI Business PDF Report
    Works with ANY CSV
    """

    pdf = SimpleDocTemplate("Business_Report.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    # ======================
    # TITLE PAGE
    # ======================
    content.append(Paragraph("AI Executive Business Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph(
        f"Total Records: {len(df)}<br/>"
        f"Total Columns: {len(df.columns)}",
        styles["Normal"]
    ))

    content.append(Spacer(1, 20))

    # ======================
    # KPI SUMMARY (AUTO)
    # ======================
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        content.append(Paragraph("Key Performance Indicators (Auto Detected)", styles["Heading2"]))
        kpi_table = [["Metric", "Sum", "Mean", "Min", "Max"]]

        for col in numeric_cols[:5]:
            kpi_table.append([
                col,
                round(df[col].sum(), 2),
                round(df[col].mean(), 2),
                round(df[col].min(), 2),
                round(df[col].max(), 2),
            ])

        table = Table(kpi_table, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)
        ]))
        content.append(table)

    # ======================
    # CHART (AUTO)
    # ======================
    if numeric_cols:
        best_col = max(numeric_cols, key=lambda c: df[c].var())

        plt.figure(figsize=(6, 4))
        plt.plot(df[best_col], marker="o")
        plt.title(f"{best_col} Trend")
        plt.xlabel("Index")
        plt.ylabel(best_col)
        plt.tight_layout()
        plt.savefig("auto_chart.png")
        plt.close()

        content.append(Spacer(1, 20))
        content.append(Image("auto_chart.png", width=400, height=250))

    # ======================
    # PREDICTION SECTION
    # ======================
    if predictions:
        content.append(PageBreak())
        content.append(Paragraph("AI Predictions", styles["Heading1"]))
        content.append(Spacer(1, 10))

        for col, pred in predictions.items():
            content.append(Paragraph(
                f"Predicted next value for <b>{col}</b>: {pred}",
                styles["Normal"]
            ))

    # ======================
    # INSIGHTS SECTION
    # ======================
    content.append(PageBreak())
    content.append(Paragraph("Executive Insights & Conclusion", styles["Heading1"]))
    content.append(Spacer(1, 10))

    insight_text = (
        "This report was automatically generated using an AI-powered business intelligence system. "
        "The system analyzes numeric trends, detects key metrics, and provides forward-looking "
        "predictions to support data-driven decision making."
    )

    content.append(Paragraph(insight_text, styles["Normal"]))

    # ======================
    # BUILD PDF
    # ======================
    pdf.build(content)

    if os.path.exists("auto_chart.png"):
        os.remove("auto_chart.png")
