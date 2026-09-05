from extensions import mysql
import re
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

# =====================================
# Admin Profile
# =====================================

@admin.route('/profile')
def profile():

    # Allow only logged-in admins
    if 'user_id' not in session or session.get('role') != 'admin':

        flash(
            'Please login to access the admin profile.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    return render_template(
        'common/profile.html',
        full_name=session.get('full_name'),
        email=session.get('email'),
        role='Admin',
        user_id=session.get('user_id'),
        dashboard_url=url_for('admin.dashboard'),
        logout_url=url_for('auth.logout'),
        change_password_url=url_for('admin.change_password')
    )

# =====================================
# Reset Mayor Password
# =====================================

@admin.route('/reset-mayor-password/<int:user_id>', methods=['GET', 'POST'])
def reset_mayor_password(user_id):

    # Allow only admins
    if 'user_id' not in session or session.get('role') != 'admin':

        flash(
            'Please login as admin.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Get selected mayor account
    cursor.execute(
        """
        SELECT user_id, full_name, email
        FROM users
        WHERE user_id=%s AND role='mayor'
        """,
        (user_id,)
    )

    mayor = cursor.fetchone()

    # If mayor not found
    if not mayor:

        cursor.close()

        flash(
            'Mayor account not found.',
            'danger'
        )

        return redirect(url_for('admin.users'))

    if request.method == 'POST':

        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Password mismatch
        if new_password != confirm_password:

            flash(
                'Passwords do not match.',
                'danger'
            )

            cursor.close()

            return redirect(
                url_for('admin.reset_mayor_password', user_id=user_id)
            )

        # Prevent using the same password again
        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE user_id=%s
            """,
            (user_id,)
        )

        current_password = cursor.fetchone()[0]

        if check_password_hash(current_password, new_password):

            cursor.close()

            flash(
                'You cannot use the same password again.',
                'warning'
            )

            return redirect(
                url_for('admin.reset_mayor_password', user_id=user_id)
            )

        # Update password
        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            """
            UPDATE users
            SET password=%s
            WHERE user_id=%s
            """,
            (hashed_password, user_id)
        )

        mysql.connection.commit()

        cursor.close()

        flash(
            f'Password for Mayor {mayor[1]} has been reset successfully.',
            'success'
        )

        return redirect(url_for('admin.users'))

    cursor.close()

    return render_template(
        'admin/reset_mayor_password.html',
        mayor=mayor
    )
# =====================================
# Admin Change Password
# =====================================

@admin.route('/change-password', methods=['POST'])
def change_password():

    # Allow only logged-in admins
    if 'user_id' not in session or session.get('role') != 'admin':

        flash(
            'Please login to change your password.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    # Check password confirmation
    if new_password != confirm_password:

        flash(
            'New password and confirm password do not match.',
            'danger'
        )

        return redirect(url_for('admin.profile'))

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

        return redirect(url_for('admin.profile'))

    stored_password_hash = user[0]

    # Verify current password
    if not check_password_hash(stored_password_hash, current_password):

        cursor.close()

        flash(
            'Current password is incorrect.',
            'danger'
        )

        return redirect(url_for('admin.profile'))

    # Prevent using the same password again
    if check_password_hash(stored_password_hash, new_password):

        cursor.close()

        flash(
            'You cannot use the password you are already using.',
            'warning'
        )

        return redirect(url_for('admin.profile'))

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
        'Admin password updated successfully.',
        'success'
    )

    return redirect(url_for('admin.profile'))

@admin.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Dashboard Cards
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM departments")
    total_departments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM wards")
    total_wards = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM budgets")
    total_budgets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM announcements")
    total_announcements = cursor.fetchone()[0]

    # Project Status Analytics
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM projects
        GROUP BY status
    """)
    project_status = cursor.fetchall()

    # Complaint Status Analytics
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM complaints
        GROUP BY status
    """)
    complaint_status = cursor.fetchall()

    # Latest Announcements
    cursor.execute("""
        SELECT title, publish_date
        FROM announcements
        ORDER BY created_at DESC
        LIMIT 5
    """)
    latest_announcements = cursor.fetchall()

    # Recent Pending Complaints
    cursor.execute("""
        SELECT title, status
        FROM complaints
        WHERE status != 'Resolved'
        ORDER BY complaint_id DESC
        LIMIT 5
    """)
    recent_complaints = cursor.fetchall()

    # Notification counts for navbar
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Ongoing'")
    ongoing_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Completed'")
    completed_projects = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        "admin/dashboard.html",
        full_name=session.get("full_name"),

        total_users=total_users,
        total_departments=total_departments,
        total_wards=total_wards,
        total_projects=total_projects,
        total_budgets=total_budgets,
        total_complaints=total_complaints,
        total_announcements=total_announcements,

        project_status=project_status,
        complaint_status=complaint_status,

        latest_announcements=latest_announcements,
        recent_complaints=recent_complaints,

        pending_complaints=pending_complaints,
        ongoing_projects=ongoing_projects,
        completed_projects=completed_projects
    )

@admin.route('/users')
def users():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    # -----------------------------
    # Total records (for pagination)
    # -----------------------------

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE full_name LIKE %s
               OR email LIKE %s
               OR role LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

        total_users = cursor.fetchone()[0]

        cursor.execute("""
            SELECT user_id,
                   full_name,
                   email,
                   role,
                   status
            FROM users
            WHERE full_name LIKE %s
               OR email LIKE %s
               OR role LIKE %s
            ORDER BY user_id
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("""
            SELECT user_id,
                   full_name,
                   email,
                   role,
                   status
            FROM users
            ORDER BY user_id
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    users = cursor.fetchall()

    # -----------------------------
    # Dashboard Cards
    # -----------------------------

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    total_admins = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='mayor'")
    total_mayors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='staff'")
    total_staff = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='citizen'")
    total_citizens = cursor.fetchone()[0]

    cursor.close()

    total_pages = (total_users + per_page - 1) // per_page

    # -----------------------------
    # Showing X - Y of Z
    # -----------------------------

    start_record = offset + 1 if total_users > 0 else 0
    end_record = min(offset + per_page, total_users)

    return render_template(
        "admin/users.html",
        users=users,
        search=search,
        page=page,
        total_pages=total_pages,
        total_users=total_users,
        total_admins=total_admins,
        total_mayors=total_mayors,
        total_staff=total_staff,
        total_citizens=total_citizens,
        start_record=start_record,
        end_record=end_record,
        full_name=session.get("full_name")
    )

@admin.route('/users/add', methods=['GET', 'POST'])
def add_user():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    error = None

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        role = request.form["role"]
        status = request.form["status"]

        # Validate Nepal mobile number
        if not re.fullmatch(r'9[78]\d{8}', phone):
            flash(
                "Please enter a valid 10-digit phone number starting with 97 or 98.",
                "danger"
            )
            return redirect(url_for("admin.add_user"))

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()

        # Check if email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()
            error = "Email already exists. Please use another email."

        else:

            cursor.execute("""
                INSERT INTO users
                (full_name, email, phone, password, role, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                full_name,
                email,
                phone,
                hashed_password,
                role,
                status
            ))

            mysql.connection.commit()
            cursor.close()

            flash("User added successfully!", "success")
            return redirect(url_for("admin.users"))

    return render_template(
        "admin/add_user.html",
        full_name=session.get("full_name"),
        error=error
    )

@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]
        role = request.form["role"]
        status = request.form["status"]

        # Validate Nepal mobile number
        if not re.fullmatch(r'9[78]\d{8}', phone):
            cursor.close()
            flash(
                "Please enter a valid 10-digit phone number starting with 97 or 98.",
                "danger"
            )
            return redirect(url_for("admin.edit_user", user_id=user_id))

        cursor.execute("""
            UPDATE users
            SET full_name=%s,
                phone=%s,
                role=%s,
                status=%s
            WHERE user_id=%s
        """, (
            full_name,
            phone,
            role,
            status,
            user_id
        ))

        mysql.connection.commit()
        cursor.close()

        flash("User updated successfully!", "success")
        return redirect(url_for("admin.users"))

    cursor.execute("""
        SELECT user_id,
               full_name,
               email,
               phone,
               role,
               status
        FROM users
        WHERE user_id=%s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()

    if not user:
        return "User not found"

    return render_template(
        "admin/edit_user.html",
        user=user,
        full_name=session.get("full_name")
    )
@admin.route('/users/delete/<int:user_id>')
def delete_user(user_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Prevent deleting yourself
    if session.get("user_id") == user_id:

        cursor.close()

        return "You cannot delete your own account."

    cursor.execute(
        "DELETE FROM users WHERE user_id=%s",
        (user_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.users"))