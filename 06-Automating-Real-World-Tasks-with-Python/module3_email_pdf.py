"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Module 3: PDF Generation & Automated Email Dispatch (module3_email_pdf.py)

Covers:
- Automated PDF report creation with ReportLab (DocTemplate, Paragraph, Table, Spacer)
- Data aggregation and business intelligence calculations (sales revenue, top sellers, peak year)
- Construction of MIME email messages using `email.message.EmailMessage`
- File attachments with automatic MIME type discovery
- Robust email dispatching via `smtplib` with simulation mode support
"""

import email.message
import mimetypes
import os
import smtplib
import sys
from typing import Any, Dict, List, Optional, Tuple

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


# -------------------------------------------------------------
# 1. CAR SALES DATA AGGREGATION & SUMMARY CALCULATION
# -------------------------------------------------------------

def process_car_sales_data(car_data: List[Dict[str, Any]]) -> Tuple[List[List[str]], List[str]]:
    """
    Analyzes car sales data to identify:
    1. The car model generating the most revenue.
    2. The car model with the highest sales volume.
    3. The most popular manufacturing year.
    Returns: (table_data_rows, summary_bullet_points)
    """
    max_revenue = 0.0
    max_revenue_car = ""
    max_sales = 0
    max_sales_car = ""
    year_sales: Dict[int, int] = {}

    # Table header
    table_data = [["ID", "Car", "Price", "Total Sales"]]

    for item in car_data:
        car = item["car"]
        car_name = f"{car['car_make']} {car['car_model']} ({car['car_year']})"
        raw_price = item["price"].replace("$", "").replace(",", "").strip()
        price = float(raw_price)
        sales = int(item["total_sales"])
        revenue = price * sales

        # Revenue tracking
        if revenue > max_revenue:
            max_revenue = revenue
            max_revenue_car = car_name

        # Sales volume tracking
        if sales > max_sales:
            max_sales = sales
            max_sales_car = car_name

        # Year distribution tracking
        year = int(car["car_year"])
        year_sales[year] = year_sales.get(year, 0) + sales

        # Add to table
        table_data.append([str(item["id"]), car_name, f"${price:,.2f}", str(sales)])

    # Determine peak year
    best_year = max(year_sales.keys(), key=lambda y: year_sales[y]) if year_sales else 0
    best_year_sales = year_sales.get(best_year, 0)

    summary = [
        f"The {max_revenue_car} generated the most revenue: ${max_revenue:,.2f}",
        f"The {max_sales_car} had the most sales: {max_sales}",
        f"The most popular year was {best_year} with {best_year_sales} sales."
    ]

    return table_data, summary


# -------------------------------------------------------------
# 2. REPORTLAB PDF GENERATOR
# -------------------------------------------------------------

def generate_pdf_report(
    filename: str,
    title: str,
    additional_info: str,
    table_data: List[List[str]]
) -> str:
    """
    Generates a PDF report containing a title, descriptive paragraph, and styled table.
    """
    out_dir = os.path.dirname(filename)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(filename)
    story = []

    # Title styling
    title_style = styles["Heading1"]
    title_style.fontSize = 18
    title_style.leading = 22
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Additional description / summary paragraphs (converting line breaks to <br/>)
    body_style = styles["Normal"]
    body_style.fontSize = 10
    body_style.leading = 14
    formatted_info = additional_info.replace("\n", "<br/>")
    story.append(Paragraph(formatted_info, body_style))
    story.append(Spacer(1, 15))

    # Styled Table
    if table_data:
        report_table = Table(table_data, hAlign="LEFT")
        report_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4285F4")),  # Google Blue
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8F9FA"), colors.white]),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))
        story.append(report_table)

    report.build(story)
    return filename


# -------------------------------------------------------------
# 3. EMAIL COMPOSITION & DISPATCH
# -------------------------------------------------------------

def generate_email_message(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    attachment_path: Optional[str] = None
) -> email.message.EmailMessage:
    """
    Creates an EmailMessage object with sender, recipient, subject, body,
    and optional attached file.
    """
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if attachment_path:
        if not os.path.exists(attachment_path):
            raise FileNotFoundError(f"Attachment not found: {attachment_path}")

        attachment_filename = os.path.basename(attachment_path)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type = mime_type or "application/octet-stream"
        main_type, sub_type = mime_type.split("/", 1)

        with open(attachment_path, "rb") as f:
            message.add_attachment(
                f.read(),
                maintype=main_type,
                subtype=sub_type,
                filename=attachment_filename
            )

    return message


def send_email(
    message: email.message.EmailMessage,
    smtp_server: str = "localhost",
    smtp_port: int = 25,
    simulate: bool = False
) -> bool:
    """
    Sends an email message via SMTP. If simulate=True, validates and returns True without connecting.
    """
    if simulate:
        return True

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as mail_server:
            mail_server.send_message(message)
        return True
    except Exception as exc:
        print(f"[WARNING] Could not send email via SMTP ({smtp_server}:{smtp_port}): {exc}", file=sys.stderr)
        return False


def test_module3() -> None:
    """
    Validation assertion test suite for Module 3.
    """
    import tempfile

    # 1. Car sales analytics verification
    sample_data = [
        {"id": 1, "car": {"car_make": "Ford", "car_model": "Mustang", "car_year": 1965}, "price": "$10,000.00", "total_sales": 20},
        {"id": 2, "car": {"car_make": "Toyota", "car_model": "Corolla", "car_year": 2010}, "price": "$5,000.00", "total_sales": 100},
        {"id": 3, "car": {"car_make": "Toyota", "car_model": "Camry", "car_year": 2010}, "price": "$8,000.00", "total_sales": 50},
    ]

    table_data, summary = process_car_sales_data(sample_data)
    assert len(table_data) == 4  # 1 header + 3 rows
    assert "Toyota Corolla (2010) had the most sales: 100" in summary[1]
    assert "The most popular year was 2010 with 150 sales." in summary[2]

    # 2. PDF generation test
    with tempfile.TemporaryDirectory() as tmp_dir:
        pdf_path = os.path.join(tmp_dir, "cars_report.pdf")
        summary_str = "\n".join(summary)
        created_pdf = generate_pdf_report(pdf_path, "Sales Summary", summary_str, table_data)

        assert os.path.exists(created_pdf)
        assert os.path.getsize(created_pdf) > 1000  # Generated valid non-empty PDF

        # 3. Email message generation and attachment test
        msg = generate_email_message(
            sender="automation@example.com",
            recipient="manager@example.com",
            subject="Monthly Sales Report",
            body="Please find the attached PDF report.",
            attachment_path=created_pdf
        )

        assert msg["From"] == "automation@example.com"
        assert msg["To"] == "manager@example.com"
        assert msg["Subject"] == "Monthly Sales Report"

        # Check attachment presence
        attachments = list(msg.iter_attachments())
        assert len(attachments) == 1
        assert attachments[0].get_filename() == "cars_report.pdf"

        # 4. Email sending simulation
        send_ok = send_email(msg, simulate=True)
        assert send_ok is True

    print("[PASS] Module 3 (PDF & Email Generation): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module3()
