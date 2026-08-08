from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

wards = Blueprint(
    'wards',
    __name__,
    url_prefix='/wards'
)


@wards.route('/')
def ward_list():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM wards
            WHERE ward_number LIKE %s
               OR ward_name LIKE %s
               OR ward_chairperson LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

        total_wards = cursor.fetchone()[0]

        cursor.execute("""
            SELECT ward_id,
                   ward_number,
                   ward_name,
                   office_address,
                   ward_chairperson,
                   created_at
            FROM wards
            WHERE ward_number LIKE %s
               OR ward_name LIKE %s
               OR ward_chairperson LIKE %s
            ORDER BY ward_number
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        cursor.execute("SELECT COUNT(*) FROM wards")
        total_wards = cursor.fetchone()[0]

        cursor.execute("""
            SELECT ward_id,
                   ward_number,
                   ward_name,
                   office_address,
                   ward_chairperson,
                   created_at
            FROM wards
            ORDER BY ward_number
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    wards_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_wards + per_page - 1) // per_page

    start_record = offset + 1 if total_wards > 0 else 0
    end_record = min(offset + per_page, total_wards)

    return render_template(
        "admin/wards.html",
        wards=wards_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_wards=total_wards,
        start_record=start_record,
        end_record=end_record,
        full_name=session.get("full_name")
    )
# ==========================================
# ADD WARD
# ==========================================

@wards.route('/add', methods=['GET', 'POST'])
def add_ward():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    error = None

    if request.method == "POST":

        ward_number = request.form["ward_number"]
        ward_name = request.form["ward_name"]
        office_address = request.form["office_address"]
        ward_chairperson = request.form["ward_chairperson"]

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT ward_id FROM wards WHERE ward_number=%s",
            (ward_number,)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.close()
            error = "Ward number already exists."

        else:

            cursor.execute("""
                INSERT INTO wards
                (ward_number, ward_name, office_address, ward_chairperson)
                VALUES (%s, %s, %s, %s)
            """, (
                ward_number,
                ward_name,
                office_address,
                ward_chairperson
            ))

            mysql.connection.commit()
            cursor.close()

            flash("Ward added successfully!", "success")
            return redirect(url_for("wards.ward_list"))

    return render_template(
        "admin/add_ward.html",
        error=error,
        full_name=session.get("full_name")
    )


# ==========================================
# EDIT WARD
# ==========================================

@wards.route('/edit/<int:ward_id>', methods=['GET', 'POST'])
def edit_ward(ward_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    if request.method == "POST":

        ward_number = request.form["ward_number"]
        ward_name = request.form["ward_name"]
        office_address = request.form["office_address"]
        ward_chairperson = request.form["ward_chairperson"]

        cursor.execute("""
            UPDATE wards
            SET ward_number=%s,
                ward_name=%s,
                office_address=%s,
                ward_chairperson=%s
            WHERE ward_id=%s
        """, (
            ward_number,
            ward_name,
            office_address,
            ward_chairperson,
            ward_id
        ))

        mysql.connection.commit()
        cursor.close()

        flash("Ward updated successfully!", "success")
        return redirect(url_for("wards.ward_list"))

    cursor.execute("""
        SELECT ward_id,
               ward_number,
               ward_name,
               office_address,
               ward_chairperson
        FROM wards
        WHERE ward_id=%s
    """, (ward_id,))

    ward = cursor.fetchone()

    cursor.close()

    if not ward:
        return "Ward not found"

    return render_template(
        "admin/edit_ward.html",
        ward=ward,
        full_name=session.get("full_name")
    )


# ==========================================
# DELETE WARD
# ==========================================

@wards.route('/delete/<int:ward_id>')
def delete_ward(ward_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM wards WHERE ward_id=%s",
        (ward_id,)
    )

    mysql.connection.commit()
    cursor.close()

    flash("Ward deleted successfully!", "success")

    return redirect(url_for("wards.ward_list"))
