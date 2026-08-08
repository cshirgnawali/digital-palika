from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import date
announcements = Blueprint(
    "announcements",
    __name__,
    url_prefix="/announcements"
)


@announcements.route("/")
def announcement_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    # =============================
    # Statistics
    # =============================

    cursor.execute("SELECT COUNT(*) FROM announcements")
    total_announcements = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM announcements
        WHERE expiry_date IS NULL
           OR expiry_date >= CURDATE()
    """)
    active = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM announcements
        WHERE expiry_date < CURDATE()
    """)
    expired = cursor.fetchone()[0]

    # =============================
    # Search
    # =============================

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM announcements
            WHERE title LIKE %s
               OR description LIKE %s
        """,(
            f"%{search}%",
            f"%{search}%"
        ))

        total_filtered = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                a.announcement_id,
                a.title,
                a.description,
                u.full_name,
                a.publish_date,
                a.expiry_date
            FROM announcements a
            JOIN users u
                ON a.published_by=u.user_id
            WHERE
                a.title LIKE %s
                OR a.description LIKE %s
            ORDER BY a.announcement_id DESC
            LIMIT %s OFFSET %s
        """,(
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        total_filtered = total_announcements

        cursor.execute("""
            SELECT
                a.announcement_id,
                a.title,
                a.description,
                u.full_name,
                a.publish_date,
                a.expiry_date
            FROM announcements a
            JOIN users u
                ON a.published_by=u.user_id
            ORDER BY a.announcement_id DESC
            LIMIT %s OFFSET %s
        """,(
            per_page,
            offset
        ))

    announcements_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_filtered + per_page - 1) // per_page

    start_record = offset + 1 if total_filtered > 0 else 0
    end_record = min(offset + per_page, total_filtered)

    return render_template(
        "admin/announcements.html",
        announcements=announcements_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_announcements=total_announcements,
        active=active,
        expired=expired,
        total_filtered=total_filtered,
        start_record=start_record,
        end_record=end_record,
        today=date.today(),
        full_name=session.get("full_name")
    )
@announcements.route('/view/<int:announcement_id>')
def view_announcement(announcement_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT announcement_id,
               title,
               description,
               published_by,
               publish_date,
               expiry_date
        FROM announcements
        WHERE announcement_id = %s
    """, (announcement_id,))

    announcement = cursor.fetchone()
    cursor.close()

    if not announcement:
        flash('Announcement not found.', 'danger')
        return redirect(url_for('announcements.announcement_list'))

    return render_template(
        'admin/view_announcement.html',
        announcement=announcement,
        full_name=session.get('full_name')
    )
# ==========================================
# ADD ANNOUNCEMENT
# ==========================================

@announcements.route('/add', methods=['GET', 'POST'])
def add_announcement():

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

    error = None

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        published_by = request.form["published_by"]
        publish_date = request.form["publish_date"]
        expiry_date = request.form["expiry_date"]

        cursor.execute("""
            INSERT INTO announcements
            (
                title,
                description,
                published_by,
                publish_date,
                expiry_date
            )
            VALUES (%s,%s,%s,%s,%s)
        """,(
            title,
            description,
            published_by,
            publish_date,
            expiry_date
        ))

        mysql.connection.commit()

        cursor.close()

        flash("Announcement added successfully!", "success")

        return redirect(url_for("announcements.announcement_list"))

    cursor.close()

    return render_template(
        "admin/add_announcement.html",
        users=users,
        error=error,
        full_name=session.get("full_name")
    )


# ==========================================
# EDIT ANNOUNCEMENT
# ==========================================

@announcements.route('/edit/<int:announcement_id>', methods=['GET', 'POST'])
def edit_announcement(announcement_id):

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

    if request.method == "POST":

        cursor.execute("""
            UPDATE announcements
            SET
                title=%s,
                description=%s,
                published_by=%s,
                publish_date=%s,
                expiry_date=%s
            WHERE announcement_id=%s
        """,(
            request.form["title"],
            request.form["description"],
            request.form["published_by"],
            request.form["publish_date"],
            request.form["expiry_date"],
            announcement_id
        ))

        mysql.connection.commit()

        flash("Announcement updated successfully!", "success")

        return redirect(url_for("announcements.announcement_list"))

    cursor.execute("""
        SELECT *
        FROM announcements
        WHERE announcement_id=%s
    """,(announcement_id,))

    announcement = cursor.fetchone()

    cursor.close()

    return render_template(
        "admin/edit_announcement.html",
        announcement=announcement,
        users=users,
        full_name=session.get("full_name")
    )


# ==========================================
# DELETE ANNOUNCEMENT
# ==========================================

@announcements.route('/delete/<int:announcement_id>')
def delete_announcement(announcement_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM announcements WHERE announcement_id=%s",
        (announcement_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Announcement deleted successfully!", "success")

    return redirect(url_for("announcements.announcement_list"))