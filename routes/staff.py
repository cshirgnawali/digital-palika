from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from extensions import mysql
from werkzeug.security import check_password_hash, generate_password_hash

staff = Blueprint('staff', __name__, url_prefix='/staff')


# ==================================================
# ACCESS CHECK
# ==================================================

def check_staff_access():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'staff':
        return 'Access Denied'

    return None
# =====================================
# Staff Profile
# =====================================

@staff.route('/profile')
def profile():

    access = check_staff_access()

    if access:
        return access

    return render_template(
        'common/profile.html',
        full_name=session.get('full_name'),
        email=session.get('email'),
        role='Staff',
        user_id=session.get('user_id'),
        dashboard_url=url_for('staff.dashboard'),
        logout_url=url_for('auth.logout'),
        change_password_url=url_for('staff.change_password')
    )
# =====================================
# Staff Change Password
# =====================================

@staff.route('/change-password', methods=['POST'])
def change_password():

    access = check_staff_access()

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

        return redirect(url_for('staff.profile'))

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

        return redirect(url_for('staff.profile'))

    stored_password_hash = user[0]

    # Verify current password
    if not check_password_hash(stored_password_hash, current_password):

        cursor.close()

        flash(
            'Current password is incorrect.',
            'danger'
        )

        return redirect(url_for('staff.profile'))

    # Prevent using the same password again
    if check_password_hash(stored_password_hash, new_password):

        cursor.close()

        flash(
            'You cannot use the password you are already using.',
            'warning'
        )

        return redirect(url_for('staff.profile'))

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
        'Staff password updated successfully.',
        'success'
    )

    return redirect(url_for('staff.profile'))

# ==================================================
# STAFF DASHBOARD
# ==================================================

@staff.route('/dashboard')
def dashboard():

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # Statistics
    cursor.execute('SELECT COUNT(*) FROM projects')
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Ongoing'")
    ongoing_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status != 'Resolved'")
    pending_complaints = cursor.fetchone()[0]

    # Latest announcements
    cursor.execute("""
        SELECT title, publish_date
        FROM announcements
        ORDER BY created_at DESC
        LIMIT 5
    """)
    latest_announcements = cursor.fetchall()

    # Latest unresolved complaints
    cursor.execute("""
        SELECT title, status
        FROM complaints
        WHERE status != 'Resolved'
        ORDER BY complaint_id DESC
        LIMIT 5
    """)
    recent_complaints = cursor.fetchall()

    cursor.close()

    return render_template(
        'staff/dashboard.html',
        total_projects=total_projects,
        ongoing_projects=ongoing_projects,
        pending_complaints=pending_complaints,
        latest_announcements=latest_announcements,
        recent_complaints=recent_complaints,
        full_name=session.get('full_name')
    )


# ==================================================
# STAFF PROJECTS
# ==================================================

@staff.route('/projects')
def projects():

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            project_name,
            status,
            estimated_cost,
            priority,
            mayor_remark,
            project_id
        FROM projects
        ORDER BY project_id DESC
    """)

    projects = cursor.fetchall()

    cursor.close()

    return render_template(
        'staff/projects.html',
        projects=projects,
        full_name=session.get('full_name')
    )


# ==================================================
# UPDATE PROJECT STATUS
# ==================================================

@staff.route('/projects/<int:project_id>/update', methods=['GET', 'POST'])
def update_project(project_id):

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        status = request.form['status']

        cursor.execute("""
            UPDATE projects
            SET status=%s
            WHERE project_id=%s
        """, (status, project_id))

        mysql.connection.commit()
        cursor.close()

        flash('Project status updated successfully!', 'success')

        return redirect(url_for('staff.projects'))

    cursor.execute("""
        SELECT project_id, project_name, status
        FROM projects
        WHERE project_id=%s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.close()

    return render_template(
        'staff/update_project.html',
        project=project,
        full_name=session.get('full_name')
    )


# ==================================================
# ADD PROGRESS UPDATE
# ==================================================

@staff.route('/projects/<int:project_id>/progress', methods=['GET', 'POST'])
def add_progress(project_id):

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        update_text = request.form['update_text']

        cursor.execute("""
            INSERT INTO project_updates
            (project_id, staff_id, update_text)
            VALUES (%s, %s, %s)
        """, (
            project_id,
            session['user_id'],
            update_text
        ))

        mysql.connection.commit()
        cursor.close()

        flash('Progress update submitted successfully!', 'success')

        return redirect(url_for('staff.projects'))

    cursor.execute("""
        SELECT project_id, project_name
        FROM projects
        WHERE project_id=%s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.close()

    return render_template(
        'staff/add_progress.html',
        project=project,
        full_name=session.get('full_name')
    )
@staff.route('/projects/<int:project_id>/updates')
def view_updates(project_id):

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT project_name
        FROM projects
        WHERE project_id=%s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.execute("""
        SELECT update_text, update_date
        FROM project_updates
        WHERE project_id=%s
        ORDER BY update_date DESC
    """, (project_id,))

    updates = cursor.fetchall()

    cursor.close()

    return render_template(
        'staff/view_updates.html',
        project=project,
        updates=updates,
        full_name=session.get('full_name')
    )


# ==================================================
# STAFF BUDGETS
# ==================================================

@staff.route('/budgets')
def budgets():

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            b.budget_id,
            p.project_name,
            b.fiscal_year,
            b.allocated_amount,
            b.spent_amount
        FROM budgets b
        JOIN projects p ON b.project_id = p.project_id
        ORDER BY b.fiscal_year DESC
    """)

    budgets = cursor.fetchall()

    cursor.close()

    return render_template(
        'staff/budgets.html',
        budgets=budgets,
        full_name=session.get('full_name')
    )
@staff.route('/budgets/<int:budget_id>/update', methods=['GET', 'POST'])
def update_budget(budget_id):

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        spent_amount = request.form['spent_amount']

        cursor.execute("""
            UPDATE budgets
            SET spent_amount=%s
            WHERE budget_id=%s
        """, (spent_amount, budget_id))

        mysql.connection.commit()
        cursor.close()

        flash('Budget expenditure updated successfully!', 'success')

        return redirect(url_for('staff.budgets'))

    cursor.execute("""
        SELECT
            b.budget_id,
            p.project_name,
            b.fiscal_year,
            b.allocated_amount,
            b.spent_amount
        FROM budgets b
        JOIN projects p ON b.project_id = p.project_id
        WHERE b.budget_id=%s
    """, (budget_id,))

    budget = cursor.fetchone()

    cursor.close()

    return render_template(
        'staff/update_budget.html',
        budget=budget,
        full_name=session.get('full_name')
    )

# ==================================================
# STAFF COMPLAINTS
# ==================================================

@staff.route('/complaints')
def complaints():

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            c.complaint_id,
            c.title,
            c.priority,
            c.location,
            c.status,
            c.submitted_date,
            w.ward_name,
            c.citizen_name
        FROM complaints c
        JOIN wards w ON c.ward_id = w.ward_id
        ORDER BY c.complaint_id DESC
    """)

    complaints = cursor.fetchall()

    cursor.close()

    return render_template(
        'staff/complaints.html',
        complaints=complaints,
        full_name=session.get('full_name')
    )
# ==================================================
# UPDATE COMPLAINT STATUS
# ==================================================

@staff.route('/complaints/<int:complaint_id>/update', methods=['GET', 'POST'])
def update_complaint(complaint_id):

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    # =====================================
    # Save Updated Status
    # =====================================
    if request.method == 'POST':

        status = request.form['status']

        cursor.execute("""
            UPDATE complaints
            SET status = %s
            WHERE complaint_id = %s
        """, (status, complaint_id))

        mysql.connection.commit()
        cursor.close()

        flash('Complaint status updated successfully!', 'success')

        return redirect(url_for('staff.complaints'))

    # =====================================
    # Load Complaint Details
    # =====================================
    cursor.execute("""
        SELECT
            c.complaint_id,
            c.title,
            c.status,
            c.citizen_name,
            w.ward_name,
            c.priority,
            c.location,
            c.submitted_date,
            c.description
        FROM complaints c
        LEFT JOIN wards w
            ON c.ward_id = w.ward_id
        WHERE c.complaint_id = %s
    """, (complaint_id,))

    complaint = cursor.fetchone()

    cursor.close()

    return render_template(
        'staff/update_complaint.html',
        complaint=complaint,
        full_name=session.get('full_name')
    )
# ==================================================
# STAFF ANNOUNCEMENTS
# ==================================================

@staff.route('/announcements', methods=['GET', 'POST'])
def announcements():

    access = check_staff_access()
    if access:
        return access

    cursor = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        expiry_date = request.form['expiry_date']

        cursor.execute("""
            INSERT INTO announcements
            (title, description, published_by, publish_date, expiry_date)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (
            title,
            description,
            session['user_id'],
            expiry_date
        ))

        mysql.connection.commit()

        flash('Announcement published successfully!', 'success')

    cursor.execute("""
        SELECT
            a.title,
            a.description,
            a.publish_date,
            u.full_name
        FROM announcements a
        JOIN users u ON a.published_by = u.user_id
        ORDER BY a.created_at DESC
    """)

    announcements = cursor.fetchall()

    cursor.close()

    from datetime import date

    return render_template(
        'staff/announcements.html',
        announcements=announcements,
        current_date=date.today().isoformat(),
        full_name=session.get('full_name')
    )