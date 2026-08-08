from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import mysql
from werkzeug.security import check_password_hash, generate_password_hash

citizen = Blueprint('citizen', __name__)


# ===============================
# Citizen Dashboard
# ===============================

@citizen.route('/dashboard')
def dashboard():

    # Allow only logged-in citizens
    if 'user_id' not in session or session.get('role') != 'citizen':
        flash('Please login to access the citizen dashboard.', 'warning')
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT title, description, publish_date
        FROM announcements
        WHERE expiry_date IS NULL
           OR expiry_date >= CURDATE()
        ORDER BY created_at DESC
        LIMIT 5
    """)

    announcements = cursor.fetchall()
    cursor.close()

    return render_template(
        'citizen/dashboard.html',
        announcements=announcements,
        full_name=session.get('full_name')
    )

# ===============================
# Submit Complaint
# ===============================
@citizen.route('/submit-complaint', methods=['GET', 'POST'])
def submit_complaint():

    # Allow only logged-in citizens
    if 'user_id' not in session or session.get('role') != 'citizen':

        flash(
            'Only registered citizens can submit a complaint.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT ward_id, ward_name FROM wards ORDER BY ward_name"
    )

    wards = cursor.fetchall()

    if request.method == 'POST':

        ward_id = request.form['ward_id']
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        priority = request.form['priority']

        # -------------------------------
        # Server-side validation
        # -------------------------------
        if (
            not ward_id or
            not title or
            not description or
            not location or
            not priority
        ):

            flash(
                'Please fill all required fields.',
                'danger'
            )

            cursor.close()

            return render_template(
                'citizen/submit_complaint.html',
                wards=wards,
                full_name=session.get('full_name')
            )

        # Use logged-in citizen details automatically
        full_name = session.get('full_name')
        email = session.get('email')
        user_id = session.get('user_id')

        # Default department for public complaints
        department_id = 1

        cursor.execute("""
            INSERT INTO complaints
            (
                user_id,
                department_id,
                ward_id,
                title,
                description,
                location,
                priority,
                status,
                citizen_name,
                citizen_email,
                submitted_date
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                'Pending', %s, %s, CURDATE()
            )
        """, (
            user_id,
            department_id,
            ward_id,
            title,
            description,
            location,
            priority,
            full_name,
            email
        ))

        mysql.connection.commit()

        complaint_id = cursor.lastrowid

        cursor.close()

        flash(
            f'Complaint submitted successfully! Your Complaint ID is {complaint_id}',
            'success'
        )

        return redirect(url_for('citizen.track_complaint'))

    cursor.close()

    return render_template(
        'citizen/submit_complaint.html',
        wards=wards,
        full_name=session.get('full_name')
    )


# ===============================
# Track Complaint
# ===============================
@citizen.route('/track-complaint', methods=['GET', 'POST'])
def track_complaint():

    complaint = None

    if request.method == 'POST':

        complaint_id = request.form['complaint_id']

        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT complaint_id, title, status, submitted_date, priority, location
            FROM complaints
            WHERE complaint_id = %s
        """, (complaint_id,))

        complaint = cursor.fetchone()
        cursor.close()

    return render_template(
        'citizen/track_complaint.html',
        complaint=complaint
    )
# ===============================
# My Complaints
# ===============================

@citizen.route('/my-complaints')
def my_complaints():

    # Allow only logged-in citizens
    if 'user_id' not in session or session.get('role') != 'citizen':

        flash(
            'Please login to view your complaints.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT
            complaint_id,
            title,
            status,
            priority,
            submitted_date,
            location
        FROM complaints
        WHERE user_id=%s
        ORDER BY submitted_date DESC, complaint_id DESC
        """,
        (session.get('user_id'),)
    )

    complaints = cursor.fetchall()

    cursor.close()

    return render_template(
        'citizen/my_complaints.html',
        complaints=complaints,
        full_name=session.get('full_name')
    )
# ===============================
# View Complaint Details
# ===============================

@citizen.route('/complaint/<int:complaint_id>')
def view_complaint(complaint_id):

    if 'user_id' not in session or session.get('role') != 'citizen':

        flash(
            'Please login to view complaint details.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT
            complaint_id,
            title,
            description,
            location,
            priority,
            status,
            submitted_date
        FROM complaints
        WHERE complaint_id=%s
          AND user_id=%s
        """,
        (complaint_id, session.get('user_id'))
    )

    complaint = cursor.fetchone()

    cursor.close()

    if not complaint:

        flash(
            'Complaint not found.',
            'danger'
        )

        return redirect(url_for('citizen.my_complaints'))

    return render_template(
        'citizen/view_complaint.html',
        complaint=complaint
    )


# ===============================
# Public Announcements
# ===============================
@citizen.route('/announcements')
def announcements():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT title, description, publish_date
        FROM announcements
        WHERE expiry_date IS NULL
           OR expiry_date >= CURDATE()
        ORDER BY created_at DESC
    """)

    announcements = cursor.fetchall()
    cursor.close()

    return render_template(
        'citizen/announcements.html',
        announcements=announcements
    )
# ===============================
# Citizen Profile
# ===============================

@citizen.route('/profile')
def profile():

    # Allow only logged-in citizens
    if 'user_id' not in session or session.get('role') != 'citizen':

        flash(
            'Please login to access your profile.',
            'warning'
        )

        return redirect(url_for('auth.login'))

    return render_template(
        'citizen/profile.html',
        full_name=session.get('full_name'),
        email=session.get('email'),
        role=session.get('role'),
        user_id=session.get('user_id'),
        dashboard_url=url_for('citizen.dashboard'),
        logout_url=url_for('auth.logout'),
        change_password_url=url_for('citizen.change_password')
    )
# ===============================
# Citizen Change Password
# ===============================

@citizen.route('/change-password', methods=['POST'])
def change_password():

    # Allow only logged-in citizens
    if 'user_id' not in session or session.get('role') != 'citizen':

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

        return redirect(url_for('citizen.profile'))

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

        return redirect(url_for('citizen.profile'))

    stored_password_hash = user[0]

    # Verify current password
    if not check_password_hash(stored_password_hash, current_password):

        cursor.close()

        flash(
            'Current password is incorrect.',
            'danger'
        )

        return redirect(url_for('citizen.profile'))

    # Prevent using the same password again
    if check_password_hash(stored_password_hash, new_password):

        cursor.close()

        flash(
            'You cannot use the password you are already using.',
            'warning'
        )

        return redirect(url_for('citizen.profile'))

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
        'Password updated successfully.',
        'success'
    )

    return redirect(url_for('citizen.profile'))
# ===============================
# Citizen Logout
# ===============================
@citizen.route('/logout')
def logout():

    session.clear()

    flash('You have been logged out successfully.', 'success')

    return redirect(url_for('auth.login'))