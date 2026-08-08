from flask import Blueprint, render_template, session, redirect, url_for, make_response
from extensions import mysql

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from datetime import datetime
import io


analytics = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


# ==========================================
# ADMIN ANALYTICS DASHBOARD
# ==========================================

@analytics.route("/")
def analytics_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Dashboard Cards
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    remaining_budget = total_budget - total_spent

    # Project Status
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
    """)
    project_status = cursor.fetchall()

    # Complaint Status
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
    """)
    complaint_status = cursor.fetchall()

    # Projects by Department
    cursor.execute("""
        SELECT
            d.department_name,
            COUNT(p.project_id)
        FROM departments d
        LEFT JOIN projects p
            ON d.department_id = p.department_id
        GROUP BY d.department_name
        ORDER BY d.department_name
    """)
    projects_by_department = cursor.fetchall()

    # Budget by Project
    cursor.execute("""
        SELECT
            p.project_name,
            COALESCE(SUM(b.allocated_amount), 0) AS total_budget
        FROM projects p
        LEFT JOIN budgets b
            ON p.project_id = b.project_id
        GROUP BY p.project_id, p.project_name
        ORDER BY total_budget DESC
    """)
    budget_by_project = cursor.fetchall()

    # Projects by Ward
    cursor.execute("""
        SELECT
            w.ward_number,
            COUNT(p.project_id)
        FROM wards w
        LEFT JOIN projects p
            ON w.ward_id = p.ward_id
        GROUP BY w.ward_number
        ORDER BY w.ward_number
    """)
    projects_by_ward = cursor.fetchall()

    # Budget vs Spent by Department
    cursor.execute("""
        SELECT
            d.department_name,
            COALESCE(SUM(b.allocated_amount), 0) AS total_budget,
            COALESCE(SUM(b.spent_amount), 0) AS total_spent
        FROM departments d
        LEFT JOIN projects p
            ON d.department_id = p.department_id
        LEFT JOIN budgets b
            ON p.project_id = b.project_id
        GROUP BY d.department_name
        ORDER BY d.department_name
    """)
    budget_department = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin/analytics.html",
        full_name=session.get("full_name"),
        total_projects=total_projects,
        total_complaints=total_complaints,
        total_budget=total_budget,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        project_status=project_status,
        complaint_status=complaint_status,
        projects_by_department=projects_by_department,
        budget_by_project=budget_by_project,
        projects_by_ward=projects_by_ward,
        budget_department=budget_department
    )


# ==========================================
# EXPORT ANALYTICS PDF
# ==========================================

@analytics.route('/export/pdf')
def export_analytics_pdf():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Dashboard statistics
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    # Project status summary
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
        ORDER BY status
    """)
    project_status = cursor.fetchall()

    # Complaint status summary
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
        ORDER BY status
    """)
    complaint_status = cursor.fetchall()

    cursor.close()

    remaining_budget = total_budget - total_spent

    if total_budget > 0:
        budget_utilization = round((total_spent / total_budget) * 100, 1)
    else:
        budget_utilization = 0

    # Create PDF
    buffer = io.BytesIO()

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
    elements.append(Paragraph("<b>Digital Palika</b>", styles['Title']))
    elements.append(Paragraph("<b>Admin Analytics Report</b>", styles['Heading1']))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # Summary Table
    summary_data = [
        ['Metric', 'Value'],
        ['Total Projects', str(total_projects)],
        ['Total Complaints', str(total_complaints)],
        ['Total Budget', f"Rs. {total_budget:,.2f}"],
        ['Total Spent', f"Rs. {total_spent:,.2f}"],
        ['Remaining Budget', f"Rs. {remaining_budget:,.2f}"],
        ['Budget Utilization', f"{budget_utilization}%"]
    ]

    summary_table = Table(summary_data, colWidths=[240, 240])

    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    # Project Status Table
    elements.append(Paragraph("<b>Project Status Summary</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    project_data = [['Status', 'Total Projects']]
    for row in project_status:
        project_data.append([row[0], str(row[1])])

    project_table = Table(project_data, colWidths=[240, 240])

    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
    ]))

    elements.append(project_table)
    elements.append(Spacer(1, 24))

    # Complaint Status Table
    elements.append(Paragraph("<b>Complaint Status Summary</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    complaint_data = [['Status', 'Total Complaints']]
    for row in complaint_status:
        complaint_data.append([row[0], str(row[1])])

    complaint_table = Table(complaint_data, colWidths=[240, 240])

    complaint_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fd7e14')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
    ]))

    elements.append(complaint_table)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph(
        "<i>This analytics report was automatically generated by the Digital Palika municipal management system for administrative monitoring and executive review.</i>",
        styles['BodyText']
    ))

    # Build PDF
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Admin_Analytics_Report.pdf'

    return response