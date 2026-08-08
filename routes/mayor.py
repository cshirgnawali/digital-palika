from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask import send_file, make_response

from extensions import mysql
from werkzeug.security import check_password_hash, generate_password_hash

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from datetime import datetime
import io

mayor = Blueprint("mayor", __name__, url_prefix="/mayor")


def check_mayor_access():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role", "").lower() != "mayor":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    return None
# =====================================
# Mayor Profile
# =====================================

@mayor.route('/profile')
def profile():

    access = check_mayor_access()

    if access:
        return access

    return render_template(
        'common/profile.html',
        full_name=session.get('full_name'),
        email=session.get('email'),
        role='Mayor',
        user_id=session.get('user_id'),
        dashboard_url=url_for('mayor.dashboard'),
        logout_url=url_for('auth.logout'),
        change_password_url=url_for('mayor.change_password')
    )
# =====================================
# Mayor Change Password
# =====================================

@mayor.route('/change-password', methods=['POST'])
def change_password():

    access = check_mayor_access()

    if access:
        return access

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Check password confirmation
    if new_password != confirm_password:

        flash(
            'New password and confirm password do not match.',
            'danger'
        )

        return redirect(url_for('mayor.profile'))

    cursor = mysql.connection.cursor()

    # Get current password hash
    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE user_id=%s
        """,
        (session.get('user_id'),)
    )

    user = cursor.fetchone()

    if not user:

        cursor.close()

        flash('User account not found.', 'danger')

        return redirect(url_for('mayor.profile'))

    stored_password_hash = user[0]

    # Verify current password
    if not check_password_hash(stored_password_hash, current_password):

        cursor.close()

        flash(
            'Current password is incorrect.',
            'danger'
        )

        return redirect(url_for('mayor.profile'))

    # Prevent using the same password again
    if check_password_hash(stored_password_hash, new_password):

        cursor.close()

        flash(
            'You cannot use the password you are already using.',
            'warning'
        )

        return redirect(url_for('mayor.profile'))

    # Hash and update new password
    hashed_password = generate_password_hash(new_password)

    cursor.execute(
        """
        UPDATE users
        SET password=%s
        WHERE user_id=%s
        """,
        (hashed_password, session.get('user_id'))
    )

    mysql.connection.commit()
    cursor.close()

    flash(
        'Mayor password updated successfully.',
        'success'
    )

    return redirect(url_for('mayor.profile'))

@mayor.route("/dashboard")
def dashboard():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # =====================================
    # Dashboard Statistics
    # =====================================
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    # =====================================
    # Budget Utilization Percentage
    # =====================================
    if total_budget > 0:
        budget_utilization = round((total_spent / total_budget) * 100, 1)
    else:
        budget_utilization = 0

    # =====================================
    # Navbar Notifications
    # =====================================
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Ongoing'")
    ongoing_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Completed'")
    completed_projects = cursor.fetchone()[0]

    # =====================================
    # Latest Announcements
    # =====================================
    cursor.execute("""
        SELECT title, publish_date
        FROM announcements
        ORDER BY created_at DESC
        LIMIT 5
    """)
    latest_announcements = cursor.fetchall()

    # =====================================
    # Recent Pending Complaints
    # =====================================
    cursor.execute("""
        SELECT title, status
        FROM complaints
        WHERE status != 'Resolved'
        ORDER BY complaint_id DESC
        LIMIT 5
    """)
    recent_complaints = cursor.fetchall()

    # =====================================
    # High Priority Projects
    # =====================================
    cursor.execute("""
        SELECT project_name, status
        FROM projects
        WHERE priority='High'
        ORDER BY project_id DESC
        LIMIT 5
    """)
    high_priority_projects = cursor.fetchall()

    # =====================================
    # Analytics: Complaints by Status
    # =====================================
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
    """)
    complaint_status = cursor.fetchall()

    # =====================================
    # Analytics: Complaints by Priority
    # =====================================
    cursor.execute("""
        SELECT priority, COUNT(*)
        FROM complaints
        GROUP BY priority
        ORDER BY FIELD(priority, 'High', 'Medium', 'Low')
    """)
    complaint_priority = cursor.fetchall()

    # =====================================
    # Analytics: Complaints by Ward
    # =====================================
    cursor.execute("""
        SELECT w.ward_name, COUNT(c.complaint_id)
        FROM complaints c
        LEFT JOIN wards w ON c.ward_id = w.ward_id
        GROUP BY w.ward_name
        ORDER BY COUNT(c.complaint_id) DESC
    """)
    complaints_by_ward = cursor.fetchall()

    cursor.close()

    return render_template(
        "mayor/dashboard.html",
        full_name=session.get("full_name"),

        # Dashboard Statistics
        total_projects=total_projects,
        total_complaints=total_complaints,
        total_budget=total_budget,
        total_spent=total_spent,
        budget_utilization=budget_utilization,

        # Notifications
        pending_complaints=pending_complaints,
        ongoing_projects=ongoing_projects,
        completed_projects=completed_projects,

        # Dashboard Lists
        latest_announcements=latest_announcements,
        recent_complaints=recent_complaints,
        high_priority_projects=high_priority_projects,

        # Analytics Data
        complaint_status=complaint_status,
        complaint_priority=complaint_priority,
        complaints_by_ward=complaints_by_ward
    )

@mayor.route('/projects')
def projects():
    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
    SELECT project_name,
           status,
           estimated_cost,
           project_id
    FROM projects
    ORDER BY project_id DESC
""")

    projects = cursor.fetchall()

    cursor.close()

    return render_template(
        'mayor/projects.html',
        projects=projects,
        full_name=session.get('full_name')
    )


@mayor.route('/budgets')
def budgets():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # ==========================================
    # Budget Table Data
    # ==========================================

    cursor.execute("""
        SELECT
            p.project_name,
            b.fiscal_year,
            b.allocated_amount,
            b.spent_amount
        FROM budgets b
        JOIN projects p
            ON b.project_id = p.project_id
        ORDER BY b.allocated_amount DESC
    """)

    budgets = cursor.fetchall()

    # ==========================================
    # Dashboard Totals
    # ==========================================

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_allocated = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    cursor.close()

    # ==========================================
    # Budget Calculations
    # ==========================================

    remaining_budget = total_allocated - total_spent

    if total_allocated > 0:
        budget_utilization = round((total_spent / total_allocated) * 100, 1)
    else:
        budget_utilization = 0

    # ==========================================
    # Render Template
    # ==========================================

    return render_template(
        'mayor/budgets.html',
        budgets=budgets,
        total_allocated=total_allocated,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        budget_utilization=budget_utilization,
        full_name=session.get('full_name')
    )


@mayor.route('/complaints')
def complaints():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # ==========================================
    # Complaint List
    # ==========================================

    cursor.execute("""
        SELECT
            c.complaint_id,
            c.title,
            c.priority,
            c.status,
            w.ward_name,
            c.submitted_date
        FROM complaints c
        LEFT JOIN wards w
            ON c.ward_id = w.ward_id
        ORDER BY c.complaint_id DESC
    """)

    complaints = cursor.fetchall()

    # ==========================================
    # Dashboard Counters
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved_count = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        'mayor/complaints.html',
        complaints=complaints,
        pending_count=pending_count,
        resolved_count=resolved_count,
        full_name=session.get('full_name')
    )

@mayor.route('/complaints/<int:complaint_id>')
def complaint_details(complaint_id):

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            c.complaint_id,
            c.title,
            c.description,
            c.status,
            c.citizen_name,
            w.ward_name,
            c.priority,
            c.location,
            c.submitted_date
        FROM complaints c
        LEFT JOIN wards w ON c.ward_id = w.ward_id
        WHERE c.complaint_id = %s
    """, (complaint_id,))

    complaint = cursor.fetchone()

    cursor.close()

    return render_template(
        'mayor/complaint_details.html',
        complaint=complaint,
        full_name=session.get('full_name')
    )


@mayor.route('/analytics')
def analytics():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # ==========================================
    # Dashboard Cards
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    # ==========================================
    # Budget Calculations
    # ==========================================

    remaining_budget = total_budget - total_spent

    if total_budget > 0:
        budget_utilization = round((total_spent / total_budget) * 100, 1)
    else:
        budget_utilization = 0

    # ==========================================
    # Project Status Chart
    # ==========================================

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
    """)
    project_status = cursor.fetchall()

    # ==========================================
    # Complaint Status Chart
    # ==========================================

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
    """)
    complaint_status = cursor.fetchall()

    # ==========================================
    # Projects by Department
    # ==========================================

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

    # ==========================================
    # Budget Allocation by Project
    # ==========================================

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

    # ==========================================
    # Projects by Ward
    # ==========================================

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

    # ==========================================
    # Budget vs Spent by Department
    # ==========================================

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
        'mayor/analytics.html',

        full_name=session.get('full_name'),

        # Dashboard Cards
        total_projects=total_projects,
        total_complaints=total_complaints,
        total_budget=total_budget,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        budget_utilization=budget_utilization,

        # Charts
        project_status=project_status,
        complaint_status=complaint_status,
        projects_by_department=projects_by_department,
        budget_by_project=budget_by_project,
        projects_by_ward=projects_by_ward,
        budget_department=budget_department
    )
@mayor.route('/analytics/export/pdf')
def export_analytics_pdf():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # ==========================================
    # Dashboard Statistics
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(allocated_amount) FROM budgets")
    total_budget = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(spent_amount) FROM budgets")
    total_spent = cursor.fetchone()[0] or 0

    # ==========================================
    # Project Status Summary
    # ==========================================

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
        ORDER BY status
    """)
    project_status = cursor.fetchall()

    # ==========================================
    # Complaint Status Summary
    # ==========================================

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
        ORDER BY status
    """)
    complaint_status = cursor.fetchall()

    cursor.close()

    # ==========================================
    # Budget Calculations
    # ==========================================

    remaining_budget = total_budget - total_spent

    if total_budget > 0:
        budget_utilization = round((total_spent / total_budget) * 100, 1)
    else:
        budget_utilization = 0

    # ==========================================
    # Create PDF Document
    # ==========================================

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

    # ==========================================
    # Title
    # ==========================================

    elements.append(Paragraph(
        "<b>Digital Palika</b>",
        styles['Title']
    ))

    elements.append(Paragraph(
        "<b>Mayor Analytics Report</b>",
        styles['Heading1']
    ))

    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles['Normal']
    ))

    elements.append(Spacer(1, 20))

    # ==========================================
    # Budget Summary Table
    # ==========================================

    elements.append(Paragraph(
        "<b>Budget & Performance Summary</b>",
        styles['Heading2']
    ))

    elements.append(Spacer(1, 10))

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
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(summary_table)

    elements.append(Spacer(1, 24))

    # ==========================================
    # Project Status Section
    # ==========================================

    elements.append(Paragraph(
        "<b>Project Status Summary</b>",
        styles['Heading2']
    ))

    elements.append(Spacer(1, 10))

    project_data = [['Status', 'Total Projects']]

    for row in project_status:
        project_data.append([row[0], str(row[1])])

    project_table = Table(project_data, colWidths=[240, 240])

    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(project_table)

    elements.append(Spacer(1, 24))

    # ==========================================
    # Complaint Status Section
    # ==========================================

    elements.append(Paragraph(
        "<b>Complaint Status Summary</b>",
        styles['Heading2']
    ))

    elements.append(Spacer(1, 10))

    complaint_data = [['Status', 'Total Complaints']]

    for row in complaint_status:
        complaint_data.append([row[0], str(row[1])])

    complaint_table = Table(complaint_data, colWidths=[240, 240])

    complaint_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
            colors.HexColor('#f8f9fa'),
            colors.white
        ]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(complaint_table)

    elements.append(Spacer(1, 24))

    # ==========================================
    # Footer Note
    # ==========================================

    elements.append(Paragraph(
        "<i>This analytics report was automatically generated by the Digital Palika municipal management system for executive monitoring and administrative review.</i>",
        styles['BodyText']
    ))

    # ==========================================
    # Build PDF
    # ==========================================

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Mayor_Analytics_Report.pdf'

    return response
@mayor.route('/reports')
def reports():

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # Project summary
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
    """)
    project_summary = cursor.fetchall()

    # Budget summary
    cursor.execute("""
        SELECT
            COALESCE(SUM(allocated_amount),0),
            COALESCE(SUM(spent_amount),0)
        FROM budgets
    """)
    budget_data = cursor.fetchone()

    total_budget = budget_data[0]
    total_spent = budget_data[1]
    remaining_budget = total_budget - total_spent

    # Ward-wise projects
    cursor.execute("""
        SELECT
            w.ward_number,
            COUNT(p.project_id)
        FROM wards w
        LEFT JOIN projects p ON w.ward_id = p.ward_id
        GROUP BY w.ward_number
        ORDER BY w.ward_number
    """)
    ward_summary = cursor.fetchall()

    cursor.close()

    return render_template(
        'mayor/reports.html',
        full_name=session.get('full_name'),
        project_summary=project_summary,
        total_budget=total_budget,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        ward_summary=ward_summary
    )
@mayor.route('/reports/download')
def download_report():

    access = check_mayor_access()
    if access:
        return access

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

    cursor = mysql.connection.cursor()

    # Dashboard data
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COALESCE(SUM(allocated_amount),0),
            COALESCE(SUM(spent_amount),0)
        FROM budgets
    """)
    budget_data = cursor.fetchone()

    total_budget = budget_data[0]
    total_spent = budget_data[1]
    remaining_budget = total_budget - total_spent

    # Project status summary
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
    """)
    project_summary = cursor.fetchall()

    cursor.close()

    # =============================
    # PDF CONTENT
    # =============================

    elements.append(Paragraph(
        "<b>DIGITAL PALIKA</b>",
        styles['Title']
    ))

    elements.append(Paragraph(
        "<b>Mayor Executive Report</b>",
        styles['Heading2']
    ))

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        f"<b>Mayor:</b> {session.get('full_name')}",
        styles['BodyText']
    ))

    elements.append(Paragraph(
        "<b>Generated:</b> Municipal Executive Dashboard",
        styles['BodyText']
    ))

    elements.append(Spacer(1, 20))

    # Municipality Overview
    elements.append(Paragraph(
        "<b>Municipality Overview</b>",
        styles['Heading3']
    ))

    elements.append(Paragraph(
        f"Total Projects: <b>{total_projects}</b>",
        styles['BodyText']
    ))

    elements.append(Paragraph(
        f"Total Complaints: <b>{total_complaints}</b>",
        styles['BodyText']
    ))

    elements.append(Spacer(1, 16))

    # Budget Summary
    elements.append(Paragraph(
        "<b>Budget Summary</b>",
        styles['Heading3']
    ))

    elements.append(Paragraph(
        f"Total Budget: <b>Rs. {total_budget:,.2f}</b>",
        styles['BodyText']
    ))

    elements.append(Paragraph(
        f"Total Spent: <b>Rs. {total_spent:,.2f}</b>",
        styles['BodyText']
    ))

    elements.append(Paragraph(
        f"Remaining Budget: <b>Rs. {remaining_budget:,.2f}</b>",
        styles['BodyText']
    ))

    elements.append(Spacer(1, 16))

    # Project Status Summary
    elements.append(Paragraph(
        "<b>Project Status Summary</b>",
        styles['Heading3']
    ))

    for status, count in project_summary:
        elements.append(Paragraph(
            f"• {status}: <b>{count}</b> projects",
            styles['BodyText']
        ))

    elements.append(Spacer(1, 24))

    elements.append(Paragraph(
        "This report was automatically generated by the Digital Palika Municipality Management System.",
        styles['Italic']
    ))

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='mayor_executive_report.pdf',
        mimetype='application/pdf'
    )
@mayor.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):

    access = check_mayor_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # ==========================================
    # Save Executive Review
    # ==========================================

    if request.method == 'POST':

        priority = request.form['priority']
        mayor_remark = request.form['mayor_remark']

        cursor.execute("""
            UPDATE projects
            SET priority = %s,
                mayor_remark = %s
            WHERE project_id = %s
        """, (priority, mayor_remark, project_id))

        mysql.connection.commit()
        cursor.close()

        flash('Project executive review updated successfully!', 'success')

        return redirect(url_for('mayor.projects'))

    # ==========================================
    # Load Project Information
    # ==========================================

    cursor.execute("""
        SELECT
            project_id,
            project_name,
            priority,
            mayor_remark
        FROM projects
        WHERE project_id = %s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.close()

    # ==========================================
    # Handle Invalid Project ID
    # ==========================================

    if not project:
        flash('Project not found.', 'danger')
        return redirect(url_for('mayor.projects'))

    # ==========================================
    # Render Executive Review Page
    # ==========================================

    return render_template(
        'mayor/edit_project.html',
        project=project,
        full_name=session.get('full_name')
    )

@mayor.route('/announcements')
def announcements():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'mayor':
        return 'Access Denied'

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT a.title, a.description, a.publish_date, u.full_name
        FROM announcements a
        JOIN users u ON a.published_by = u.user_id
        ORDER BY a.created_at DESC
    """)

    announcements = cursor.fetchall()
    cursor.close()

    return render_template(
        'mayor/announcements.html',
        announcements=announcements,
        full_name=session.get('full_name')
    )