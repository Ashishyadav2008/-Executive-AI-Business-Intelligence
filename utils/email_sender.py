import os
import smtplib
from email.message import EmailMessage


def send_email(receiver_email: str, pdf_path="Business_Report.pdf"):
    """
    Send AI-generated Business Report via Email
    """

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError("Email credentials not set in environment variables")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError("PDF report not found")

    msg = EmailMessage()
    msg["Subject"] = "📊 AI Business Intelligence Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content("""
Hello,

Please find attached your AI-generated Business Intelligence Report.

This report includes:
• Auto KPIs
• Smart Trends
• AI Predictions
• Executive Insights

Regards,
AI Business Operating System
""")

    # -------- ATTACH PDF --------
    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_path)
        )

    # -------- SEND EMAIL --------
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
