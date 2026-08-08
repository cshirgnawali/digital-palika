from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

departments = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments"
)


# ==================================================
# Department List
# ==================================================

@departments.route("/")
def department_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM departments
            WHERE department_name LIKE %s
               OR description LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%"
        ))

        total_departments = cursor.fetchone()[0]

        cursor.execute("""
            SELECT department_id,
                   department_name,
                   description,
                   created_at
            FROM departments
            WHERE department_name LIKE %s
               OR description LIKE %s
            ORDER BY department_id
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        cursor.execute("SELECT COUNT(*) FROM departments")
        total_departments = cursor.fetchone()[0]

        cursor.execute("""
            SELECT department_id,
                   department_name,
                   description,
                   created_at
            FROM departments
            ORDER BY department_id
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    departments_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_departments + per_page - 1) // per_page

    start_record = offset + 1 if total_departments else 0
    end_record = min(offset + per_page, total_departments)

    return render_template(
        "admin/departments.html",
        departments=departments_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_departments=total_departments,
        start_record=start_record,
        end_record=end_record,
        full_name=session.get("full_name")
    )


# ==================================================
# Add Department
# ==================================================

@departments.route("/add", methods=["GET", "POST"])
def add_department():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    error = None

    if request.method == "POST":

        department_name = request.form["department_name"].strip()
        description = request.form["description"].strip()

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT department_id FROM departments WHERE department_name=%s",
            (department_name,)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.close()
            error = "Department already exists."

        else:

            cursor.execute("""
                INSERT INTO departments
                (department_name, description)
                VALUES (%s, %s)
            """, (
                department_name,
                description
            ))

            mysql.connection.commit()
            cursor.close()

            flash("Department added successfully!", "success")

            return redirect(url_for("departments.department_list"))

    return render_template(
        "admin/add_department.html",
        error=error,
        full_name=session.get("full_name")
    )


# ==================================================
# Edit Department
# ==================================================

@departments.route("/edit/<int:department_id>", methods=["GET", "POST"])
def edit_department(department_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        department_name = request.form["department_name"].strip()
        description = request.form["description"].strip()

        cursor.execute("""
            UPDATE departments
            SET department_name=%s,
                description=%s
            WHERE department_id=%s
        """, (
            department_name,
            description,
            department_id
        ))

        mysql.connection.commit()

        cursor.close()

        flash("Department updated successfully!", "success")

        return redirect(url_for("departments.department_list"))

    cursor.execute("""
        SELECT department_id,
               department_name,
               description
        FROM departments
        WHERE department_id=%s
    """, (department_id,))

    department = cursor.fetchone()

    cursor.close()

    if not department:
        return "Department not found"

    return render_template(
        "admin/edit_department.html",
        department=department,
        full_name=session.get("full_name")
    )


# ==================================================
# Delete Department
# ==================================================

@departments.route("/delete/<int:department_id>")
def delete_department(department_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM departments WHERE department_id=%s",
        (department_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Department deleted successfully!", "success")

    return redirect(url_for("departments.department_list"))