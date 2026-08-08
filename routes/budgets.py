from extensions import mysql
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

budgets = Blueprint(
    "budgets",
    __name__,
    url_prefix="/budgets"
)
@budgets.route("/")
def budget_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Access Denied"

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    cursor = mysql.connection.cursor()

    # ==========================
    # Statistics
    # ==========================

    cursor.execute("SELECT COUNT(*) FROM budgets")
    total_budgets = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(allocated_amount),0)
        FROM budgets
    """)
    total_allocated = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(spent_amount),0)
        FROM budgets
    """)
    total_spent = cursor.fetchone()[0]

    remaining_budget = total_allocated - total_spent

    # ==========================
    # Search
    # ==========================

    if search:

        cursor.execute("""
            SELECT COUNT(*)
            FROM budgets b
            JOIN projects p
                ON b.project_id=p.project_id
            WHERE
                p.project_name LIKE %s
                OR b.fiscal_year LIKE %s
                OR b.budget_status LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

        total_filtered = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                b.budget_id,
                p.project_name,
                b.fiscal_year,
                b.allocated_amount,
                b.spent_amount,
                b.budget_status
            FROM budgets b
            JOIN projects p
                ON b.project_id=p.project_id
            WHERE
                p.project_name LIKE %s
                OR b.fiscal_year LIKE %s
                OR b.budget_status LIKE %s
            ORDER BY b.budget_id
            LIMIT %s OFFSET %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            per_page,
            offset
        ))

    else:

        total_filtered = total_budgets

        cursor.execute("""
            SELECT
                b.budget_id,
                p.project_name,
                b.fiscal_year,
                b.allocated_amount,
                b.spent_amount,
                b.budget_status
            FROM budgets b
            JOIN projects p
                ON b.project_id=p.project_id
            ORDER BY b.budget_id
            LIMIT %s OFFSET %s
        """, (
            per_page,
            offset
        ))

    budgets_data = cursor.fetchall()

    cursor.close()

    total_pages = (total_filtered + per_page - 1) // per_page

    start_record = offset + 1 if total_filtered > 0 else 0
    end_record = min(offset + per_page, total_filtered)

    return render_template(
        "admin/budgets.html",
        budgets=budgets_data,
        search=search,
        page=page,
        total_pages=total_pages,
        total_filtered=total_filtered,
        total_budgets=total_budgets,
        total_allocated=total_allocated,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        start_record=start_record,
        end_record=end_record,
        full_name=session.get("full_name")
    )
# ==========================================
# ADD BUDGET
# ==========================================


@budgets.route('/add', methods=['GET', 'POST'])
def add_budget():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    # Load Projects Dropdown
    cursor.execute("""
        SELECT project_id, project_name
        FROM projects
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    error = None

    if request.method == "POST":

        project_id = request.form["project_id"]
        fiscal_year = request.form["fiscal_year"]
        allocated_amount = request.form["allocated_amount"]
        spent_amount = request.form["spent_amount"]
        budget_status = request.form["budget_status"]

        cursor.execute("""
            INSERT INTO budgets
            (
                project_id,
                fiscal_year,
                allocated_amount,
                spent_amount,
                budget_status
            )
            VALUES (%s,%s,%s,%s,%s)
        """,(
            project_id,
            fiscal_year,
            allocated_amount,
            spent_amount,
            budget_status
        ))

        mysql.connection.commit()

        cursor.close()

        flash("Budget added successfully!","success")

        return redirect(url_for("budgets.budget_list"))

    cursor.close()

    return render_template(
        "admin/add_budget.html",
        projects=projects,
        error=error,
        full_name=session.get("full_name")
    )


# ==========================================
# EDIT BUDGET
# ==========================================

@budgets.route('/edit/<int:budget_id>', methods=['GET', 'POST'])
def edit_budget(budget_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT project_id, project_name
        FROM projects
        ORDER BY project_name
    """)

    projects = cursor.fetchall()

    if request.method == "POST":

        cursor.execute("""
            UPDATE budgets
            SET
                project_id=%s,
                fiscal_year=%s,
                allocated_amount=%s,
                spent_amount=%s,
                budget_status=%s
            WHERE budget_id=%s
        """,(
            request.form["project_id"],
            request.form["fiscal_year"],
            request.form["allocated_amount"],
            request.form["spent_amount"],
            request.form["budget_status"],
            budget_id
        ))

        mysql.connection.commit()

        flash("Budget updated successfully!", "success")

        return redirect(url_for("budgets.budget_list"))

    cursor.execute("""
        SELECT *
        FROM budgets
        WHERE budget_id=%s
    """,(budget_id,))

    budget = cursor.fetchone()

    cursor.close()

    return render_template(
        "admin/edit_budget.html",
        budget=budget,
        projects=projects,
        full_name=session.get("full_name")
    )


# ==========================================
# DELETE BUDGET
# ==========================================

@budgets.route('/delete/<int:budget_id>')
def delete_budget(budget_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('role') != 'admin':
        return "Access Denied"

    cursor = mysql.connection.cursor()

    cursor.execute(
        "DELETE FROM budgets WHERE budget_id=%s",
        (budget_id,)
    )

    mysql.connection.commit()

    cursor.close()

    flash("Budget deleted successfully!", "success")

    return redirect(url_for("budgets.budget_list"))