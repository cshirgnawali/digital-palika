from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

complaints = Blueprint(
    "complaints",
    __name__,
    url_prefix="/complaints"
)


@complaints.route("/")
def complaint_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    # ===============================
    # Statistics
    # ===============================

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='In Progress'")
    in_progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    # ===============================
    # Search
    # ===============================

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM complaints
            WHERE title LIKE %s
               OR location LIKE %s
               OR status LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

        total_filtered = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                c.complaint_id,
                u.full_name,
                d.department_name,
                w.ward_number,
                c.title,
                c.priority,
                c.status,
                c.submitted_at
            FROM complaints c
            JOIN users u
                ON c.user_id=u.user_id
            JOIN departments d
                ON c.department_id=d.department_id
            JOIN wards w
                ON c.ward_id=w.ward_id
            WHERE
                c.title LIKE %s
                OR c.location LIKE %s
                OR c.status LIKE %s
            ORDER BY c.complaint_id DESC
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        total_filtered = total_complaints

        cursor.execute("""
            SELECT
                c.complaint_id,
                u.full_name,
                d.department_name,
                w.ward_number,
                c.title,
                c.priority,
                c.status,
                c.submitted_at
            FROM complaints c
            JOIN users u
                ON c.user_id=u.user_id
            JOIN departments d
                ON c.department_id=d.department_id
            JOIN wards w
                ON c.ward_id=w.ward_id
            ORDER BY c.complaint_id DESC
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    complaints_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_filtered + per_page - 1) // per_page

    start_record = offset + 1 if total_filtered > 0 else 0
    end_record = min(offset + per_page, total_filtered)

    return render_template(
        "admin/complaints.html",
        complaints=complaints_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_complaints=total_complaints,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        total_filtered=total_filtered,
        start_record=start_record,
        end_record=end_record,
        full_name=session.get("full_name")
    )

# ==========================================
# ADD COMPLAINT
# ==========================================

@complaints.route('/add', methods=['GET', 'POST'])
def add_complaint():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Users
    cursor.execute("""
        SELECT user_id, full_name
        FROM users
        ORDER BY full_name
    """)
    users = cursor.fetchall()

    # Departments
    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
        ORDER BY department_name
    """)
    departments = cursor.fetchall()

    # Wards
    cursor.execute("""
        SELECT ward_id, ward_number
        FROM wards
        ORDER BY ward_number
    """)
    wards = cursor.fetchall()

    error = None

    if request.method == "POST":

        user_id = request.form["user_id"]
        department_id = request.form["department_id"]
        ward_id = request.form["ward_id"]
        title = request.form["title"]
        description = request.form["description"]
        location = request.form["location"]
        priority = request.form["priority"]
        status = request.form["status"]

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
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,(
            user_id,
            department_id,
            ward_id,
            title,
            description,
            location,
            priority,
            status
        ))

        mysql.connection.commit()

        cursor.close()

        flash("Complaint added successfully!", "success")

        return redirect(url_for("complaints.complaint_list"))

    cursor.close()

    return render_template(
        "admin/add_complaint.html",
        users=users,
        departments=departments,
        wards=wards,
        error=error,
        full_name=session.get("full_name")
    )

# ==========================================
# EDIT COMPLAINT
# ==========================================

@complaints.route('/edit/<int:complaint_id>', methods=['GET', 'POST'])
def edit_complaint(complaint_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT user_id, full_name
        FROM users
        ORDER BY full_name
    """)
    users = cursor.fetchall()

    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
        ORDER BY department_name
    """)
    departments = cursor.fetchall()

    cursor.execute("""
        SELECT ward_id, ward_number
        FROM wards
        ORDER BY ward_number
    """)
    wards = cursor.fetchall()

    if request.method == "POST":

        cursor.execute("""
            UPDATE complaints
            SET
                user_id=%s,
                department_id=%s,
                ward_id=%s,
                title=%s,
                description=%s,
                location=%s,
                priority=%s,
                status=%s
            WHERE complaint_id=%s
        """,(
            request.form["user_id"],
            request.form["department_id"],
            request.form["ward_id"],
            request.form["title"],
            request.form["description"],
            request.form["location"],
            request.form["priority"],
            request.form["status"],
            complaint_id
        ))

        mysql.connection.commit()

        flash("Complaint updated successfully!", "success")

        return redirect(url_for("complaints.complaint_list"))

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE complaint_id=%s
    """,(complaint_id,))

    complaint = cursor.fetchone()

    cursor.close()

    return render_template(
        "admin/edit_complaint.html",
        complaint=complaint,
        users=users,
        departments=departments,
        wards=wards,
        full_name=session.get("full_name")
    )


# ==========================================
# DELETE COMPLAINT
# ==========================================

@complaints.route('/delete/<int:complaint_id>')
def delete_complaint(complaint_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM complaints WHERE complaint_id=%s",
        (complaint_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Complaint deleted successfully!", "success")

    return redirect(url_for("complaints.complaint_list"))