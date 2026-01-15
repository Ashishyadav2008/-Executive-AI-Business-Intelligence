import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.analysis import load_data
from utils.llm_chat import ask_llm
from utils.report import generate_report
from utils.prediction import predict_sales
from utils.voice_input import voice_to_text
from utils.email_sender import send_email
from utils.visualization import render_charts
from streamlit_extras.metric_cards import style_metric_cards

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Executive AI Business OS",
    layout="wide"
)

# ==============================
# CUSTOM CSS (POWER BI FEEL)
# ==============================
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: 700;
    color: #00E5FF !important;
}
[data-testid="stMetricLabel"] {
    font-size: 16px;
    color: #FFFFFF !important;
}
[data-testid="stMetric"] {
    background-color: #0F172A;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 0 20px rgba(0,229,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE & SIDEBAR
# ==============================
st.title("🤖 Executive AI Business Intelligence OS")

st.sidebar.title("📊 AI Data Copilot")
st.sidebar.markdown("""
### Navigation
📁 Upload CSV  
📌 KPI Dashboard  
📊 Smart Charts  
🤖 AI Insights  
🎙 Voice AI  
📄 PDF & Email  
""")

# ==============================
# CSV UPLOAD
# ==============================
st.subheader("📁 Upload Any Business CSV")
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is None:
    st.info("Please upload a CSV file to start analysis")
    st.stop()

df = load_data(file)
st.dataframe(df, use_container_width=True)

# ==============================
# COLUMN DETECTION
# ==============================
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

# ==============================
# TABS
# ==============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 KPI Dashboard",
    "📊 Executive Smart Charts",
    "🤖 AI Insights",
    "🎙 Voice AI"
])

# ==============================
# KPI DASHBOARD
# ==============================
with tab1:
    st.subheader("📌 KPI Dashboard (Auto Detected)")

    if numeric_cols:
        cols = st.columns(3)
        for i, col in enumerate(numeric_cols[:6]):
            cols[i % 3].metric(
                label=col,
                value=round(df[col].sum(), 2)
            )
        style_metric_cards()
    else:
        st.warning("No numeric columns found")

# ==============================
# SMART CHARTS
# ==============================
with tab2:
    st.subheader("📊 Executive Smart Charts")
    render_charts(df)

# ==============================
# AI INSIGHTS
# ==============================
with tab3:
    st.subheader("🤖 AI Auto Insights")

    summary = ""
    if numeric_cols:
        summary += "Numeric Summary:\n"
        for col in numeric_cols:
            summary += (
                f"{col} → "
                f"sum={df[col].sum():.2f}, "
                f"mean={df[col].mean():.2f}, "
                f"min={df[col].min():.2f}, "
                f"max={df[col].max():.2f}\n"
            )

    if categorical_cols:
        summary += "\nCategorical Summary:\n"
        for col in categorical_cols:
            top = df[col].mode()[0] if not df[col].mode().empty else "N/A"
            summary += f"{col} → most frequent: {top}\n"

    st.text_area("Dataset Overview", summary, height=250)

    question = st.text_input("Ask any business question")

    if st.button("Ask AI"):
        with st.spinner("AI analyzing data..."):
            st.success(ask_llm(question or summary, df))

# ==============================
# VOICE AI
# ==============================
with tab4:
    st.subheader("🎙 Voice Assistant")

    if st.button("🎤 Speak"):
        with st.spinner("Listening..."):
            voice_query = voice_to_text()

        if voice_query:
            st.success(f"You said: {voice_query}")
            st.success(ask_llm(voice_query, df))
        else:
            st.warning("Could not understand voice")

# ==============================
# AUTO PREDICTIONS
# ==============================
st.subheader("🔮 AI Predictions")

predictions = {}

if numeric_cols:
    result = predict_sales(df)
    if result:
        predictions[result["column"]] = result["predicted_value"]
        st.success(f"Predicted next value for {result['column']}: {result['predicted_value']}")
else:
    st.info("No numeric columns available for prediction")

st.session_state.predictions = predictions

# ==============================
# PDF REPORT & EMAIL
# ==============================
st.subheader("📄 PDF Report & Email")

email = st.text_input("📧 Enter email to send report")

if st.button("Generate PDF Report"):
    generate_report(df, st.session_state.get("predictions"))
    st.success("✅ PDF Generated")

    with open("Business_Report.pdf", "rb") as f:
        st.download_button(
            "📥 Download PDF",
            f,
            file_name="Business_Report.pdf",
            mime="application/pdf"
        )

if st.button("📧 Send Report via Email"):
    if email.strip():
        try:
            send_email(email)
            st.success("📨 Email sent successfully")
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter an email address")
