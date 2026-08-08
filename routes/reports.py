from flask import Blueprint, render_template, session, redirect, url_for, send_file
from extensions import mysql

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from io import BytesIO
from datetime import datetime


reports = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)


# =========================================================
# Reports Dashboard
# =========================================================

@reports.route("/")
def reports_dashboard():

    # Login Check
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Admin Check
    if session.get("role") != "admin":
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Recent Projects
    cursor.execute("""
        SELECT project_name, status, estimated_cost
        FROM projects
        ORDER BY project_id DESC
        LIMIT 5
    """)
    recent_projects = cursor.fetchall()

    # Recent Complaints
    cursor.execute("""
        SELECT title, status
        FROM complaints
        ORDER BY complaint_id DESC
        LIMIT 5
    """)
    recent_complaints = cursor.fetchall()

    # Budget Summary
    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    cursor.close()

    return render_template(
        "admin/reports.html",
        full_name=session.get("full_name"),
        recent_projects=recent_projects,
        recent_complaints=recent_complaints,
        total_budget=total_budget,
        total_spent=total_spent
    )


# =========================================================
# Export PDF Report
# =========================================================

@reports.route("/export-pdf")
def export_pdf():

    # Login Check
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cursor = mysql.connection.cursor()

    # Budget Summary
    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    # Recent Projects
    cursor.execute("""
        SELECT project_name, status, estimated_cost
        FROM projects
        ORDER BY project_id DESC
        LIMIT 5
    """)
    recent_projects = cursor.fetchall()

    # Recent Complaints
    cursor.execute("""
        SELECT title, status
        FROM complaints
        ORDER BY complaint_id DESC
        LIMIT 5
    """)
    recent_complaints = cursor.fetchall()

    cursor.close()

    # Create PDF in memory
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(
        "<b>Digital Palika - Municipality Report</b>",
        styles["Title"]
    ))

    elements.append(Spacer(1, 12))

    # Generated Date
    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d %B %Y %I:%M %p')}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 18))

    # Budget Summary
    elements.append(Paragraph("<b>Budget Summary</b>", styles["Heading2"]))

    elements.append(Paragraph(
        f"Total Budget: Rs. {total_budget:,.2f}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Total Spent: Rs. {total_spent:,.2f}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Remaining Budget: Rs. {total_budget - total_spent:,.2f}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 18))

    # Recent Projects
    elements.append(Paragraph("<b>Recent Projects</b>", styles["Heading2"]))

    for project in recent_projects:
        elements.append(Paragraph(
            f"• {project[0]} ({project[1]}) - Rs. {project[2]:,.2f}",
            styles["Normal"]
        ))

    elements.append(Spacer(1, 18))

    # Recent Complaints
    elements.append(Paragraph("<b>Recent Complaints</b>", styles["Heading2"]))

    for complaint in recent_complaints:
        elements.append(Paragraph(
            f"• {complaint[0]} ({complaint[1]})",
            styles["Normal"]
        ))

    elements.append(Spacer(1, 18))

    # Footer
    elements.append(Paragraph(
        "This report was generated automatically by the Digital Palika Management System.",
        styles["Italic"]
    ))

    # Build PDF
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="digital_palika_report.pdf",
        mimetype="application/pdf"
    )