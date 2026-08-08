from flask import Flask
from extensions import mysql, mail
from config import Config
from routes.auth import auth
from routes.admin import admin
from routes.mayor import mayor
from routes.staff import staff
from routes.citizen import citizen
from flask import render_template
from routes.departments import departments
from routes.wards import wards
from routes.projects import projects
from routes.budgets import budgets
from routes.complaints import complaints
from routes.announcements import announcements
from routes.analytics import analytics
from routes.reports import reports

app = Flask(__name__)
app = Flask(__name__)

# =========================
# Gmail OTP Configuration
# =========================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Gmail
app.config['MAIL_USERNAME'] = 'gnawalishishir222@gmail.com'

app.config['MAIL_PASSWORD'] = 'awzt vytk satl pquv'
app.config.from_object(Config)

mysql.init_app(app)
mail.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(departments)
app.register_blueprint(wards)
app.register_blueprint(projects)
app.register_blueprint(budgets)
app.register_blueprint(complaints)
app.register_blueprint(announcements)
app.register_blueprint(analytics)
app.register_blueprint(reports)
app.register_blueprint(mayor)
app.register_blueprint(staff)
app.register_blueprint(citizen)
# ===============================
# Error Handlers
# ===============================

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500
if __name__ == '__main__':
    app.run(debug=True) 