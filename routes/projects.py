from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

projects = Blueprint(
    "projects",
    __name__,
    url_prefix="/projects"
)


@projects.route("/")
def project_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    # Statistics
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Planned'")
    planned = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Ongoing'")
    ongoing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM projects
            WHERE project_name LIKE %s
               OR contractor_name LIKE %s
               OR status LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

        total_filtered = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                p.project_id,
                p.project_name,
                d.department_name,
                w.ward_number,
                p.estimated_cost,
                p.status,
                p.contractor_name,
                p.priority,
                p.mayor_remark
            FROM projects p
            JOIN departments d
                ON p.department_id=d.department_id
            JOIN wards w
                ON p.ward_id=w.ward_id
            WHERE
                p.project_name LIKE %s
                OR p.contractor_name LIKE %s
                OR p.status LIKE %s
            ORDER BY p.project_id
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        total_filtered = total_projects

        cursor.execute("""
            SELECT
                p.project_id,
                p.project_name,
                d.department_name,
                w.ward_number,
                p.estimated_cost,
                p.status,
                p.contractor_name,
                p.priority,
                p.mayor_remark
            FROM projects p
            JOIN departments d
                ON p.department_id=d.department_id
            JOIN wards w
                ON p.ward_id=w.ward_id
            ORDER BY p.project_id
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    projects_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_filtered + per_page - 1) // per_page

    start_record = offset + 1 if total_filtered > 0 else 0
    end_record = min(offset + per_page, total_filtered)

    return render_template(
        "admin/projects.html",
        projects=projects_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_projects=total_projects,
        planned=planned,
        ongoing=ongoing,
        completed=completed,
        start_record=start_record,
        end_record=end_record,
        total_filtered=total_filtered,
        full_name=session.get("full_name")
    )
# ==========================================
# ADD PROJECT
# ==========================================

@projects.route('/add', methods=['GET', 'POST'])
def add_project():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

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

    error = None

    if request.method == "POST":

        department_id = request.form["department_id"]
        ward_id = request.form["ward_id"]
        project_name = request.form["project_name"]
        description = request.form["description"]
        estimated_cost = request.form["estimated_cost"]
        start_date = request.form["start_date"]
        expected_end_date = request.form["expected_end_date"]
        status = request.form["status"]
        contractor_name = request.form["contractor_name"]

        # -------------------------------
        # Server-side validation
        # -------------------------------
        if (
            not department_id or
            not ward_id or
            not project_name or
            not description or
            not estimated_cost or
            not start_date or
            not expected_end_date or
            not status or
            not contractor_name
        ):

            error = "Please fill all required fields."

            flash(error, "danger")

            cursor.close()

            return render_template(
                "admin/add_project.html",
                departments=departments,
                wards=wards,
                error=error,
                full_name=session.get("full_name")
            )

        cursor.execute("""
            INSERT INTO projects
            (
                department_id,
                ward_id,
                project_name,
                description,
                estimated_cost,
                start_date,
                expected_end_date,
                status,
                contractor_name
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            department_id,
            ward_id,
            project_name,
            description,
            estimated_cost,
            start_date,
            expected_end_date,
            status,
            contractor_name
        ))

        mysql.connection.commit()

        cursor.close()

        flash("Project added successfully!", "success")

        return redirect(url_for("projects.project_list"))

    cursor.close()

    return render_template(
        "admin/add_project.html",
        departments=departments,
        wards=wards,
        error=error,
        full_name=session.get("full_name")
    )

# ==========================================
# EDIT PROJECT
# ==========================================

@projects.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

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

        department_id = request.form["department_id"]
        ward_id = request.form["ward_id"]
        project_name = request.form["project_name"]
        description = request.form["description"]
        estimated_cost = request.form["estimated_cost"]
        start_date = request.form.get("start_date")
        expected_end_date = request.form.get("expected_end_date")
        status = request.form["status"]
        contractor_name = request.form["contractor_name"]

        # -------------------------------
        # Server-side validation
        # -------------------------------
        if (
            not department_id or
            not ward_id or
            not project_name or
            not description or
            not estimated_cost or
            not start_date or
            not expected_end_date or
            not status or
            not contractor_name
        ):

            flash(
                'Please fill all required fields.',
                'danger'
            )

            cursor.close()

            return redirect(url_for('projects.edit_project', project_id=project_id))

        cursor.execute("""
            UPDATE projects
            SET
                department_id=%s,
                ward_id=%s,
                project_name=%s,
                description=%s,
                estimated_cost=%s,
                start_date=%s,
                expected_end_date=%s,
                status=%s,
                contractor_name=%s
            WHERE project_id=%s
        """, (
            department_id,
            ward_id,
            project_name,
            description,
            estimated_cost,
            start_date,
            expected_end_date,
            status,
            contractor_name,
            project_id
        ))

        mysql.connection.commit()

        flash(
            'Project updated successfully!',
            'success'
        )

        cursor.close()

        return redirect(url_for('projects.project_list'))

    cursor.execute("""
        SELECT *
        FROM projects
        WHERE project_id=%s
    """, (project_id,))

    project = cursor.fetchone()

    cursor.close()

    return render_template(
        'admin/edit_project.html',
        project=project,
        departments=departments,
        wards=wards,
        full_name=session.get('full_name')
    )

# ==========================================
# DELETE PROJECT
# ==========================================

@projects.route('/delete/<int:project_id>')
def delete_project(project_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM projects WHERE project_id=%s",
        (project_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Project deleted successfully!", "success")

    return redirect(url_for("projects.project_list"))
# ==========================================
# PROJECT UPDATES MONITORING
# ==========================================

@projects.route('/updates')
def project_updates():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return 'Access Denied'

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            p.project_name,
            u.full_name,
            pu.update_text,
            pu.update_date
        FROM project_updates pu
        JOIN projects p ON pu.project_id = p.project_id
        JOIN users u ON pu.staff_id = u.user_id
        ORDER BY pu.update_date DESC
    """)

    updates = cursor.fetchall()

    cursor.close()

    return render_template(
        'admin/project_updates.html',
        updates=updates,
        full_name=session.get('full_name')
    )
@projects.route('/announcements')
def announcements_admin():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
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
        'admin/announcements.html',
        announcements=announcements,
        full_name=session.get('full_name')
    )