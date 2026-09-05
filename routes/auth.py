from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from extensions import mysql, mail
from datetime import datetime, timedelta
import random
import re

auth = Blueprint('auth', __name__)

# ======================================
# LOGIN
# ======================================

@auth.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT
                user_id,
                full_name,
                email,
                password,
                role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user[3], password):

            session['user_id'] = user[0]
            session['full_name'] = user[1]
            session['email'] = user[2]
            session['role'] = user[4]

            return redirect(url_for(f"{user[4]}.dashboard"))

        flash('Invalid Email or Password', 'danger')

    return render_template('auth/login.html')

# ======================================
# CITIZEN REGISTRATION
# ======================================

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

# Validate Nepal mobile number
        if not re.fullmatch(r'9[78]\d{8}', mobile_number):
            flash(
                'Please enter a valid 10-digit Nepal mobile number starting with 97 or 98.',
                'danger'
            )
            return redirect(url_for('auth.register'))

        if password != confirm_password:

            flash('Passwords do not match.', 'danger')

            return redirect(url_for('auth.register'))

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE mobile_number = %s
               OR email = %s
            """,
            (mobile_number, email)
        )

        existing = cursor.fetchone()

        if existing:

            cursor.close()

            flash(
                'You are already registered with this mobile number or email.',
                'warning'
            )

            return redirect(url_for('auth.register'))

        otp = str(random.randint(100000, 999999))

        session['pending_registration'] = {
            'full_name': full_name,
            'mobile_number': mobile_number,
            'email': email,
            'password': password,
            'otp': otp,
            'expiry': (
                datetime.now() + timedelta(minutes=5)
            ).isoformat()
        }

        msg = Message(
            'Digital Palika Verification Code',
            sender='gnawalishishir222@gmail.com',
            recipients=[email]
        )

        msg.body = f'''
Hello {full_name},

Your Digital Palika verification code is:

{otp}

This code is valid for 5 minutes.

Digital Palika
Smart Municipality Management System
'''

        mail.send(msg)

        flash(
            'Verification code has been sent to your email.',
            'info'
        )

        return redirect(url_for('auth.verify_otp'))

    return render_template('auth/register.html')

# ======================================
# OTP VERIFICATION
# ======================================

@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():

    data = session.get('pending_registration')

    if not data:

        flash('Registration session expired.', 'warning')

        return redirect(url_for('auth.register'))

    if request.method == 'POST':

        entered_otp = request.form['otp']

        expiry = datetime.fromisoformat(data['expiry'])

        if datetime.now() > expiry:

            session.pop('pending_registration', None)

            flash(
                'OTP has expired. Please register again.',
                'warning'
            )

            return redirect(url_for('auth.register'))

        if entered_otp != data['otp']:

            flash('Invalid verification code.', 'danger')

            return redirect(url_for('auth.verify_otp'))

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (
                full_name,
                mobile_number,
                phone,
                email,
                password,
                role,
                status
            )
            VALUES (%s,%s,%s,%s,%s,'citizen','active')
            """,
            (
                data['full_name'],
                data['mobile_number'],
                data['mobile_number'],
                data['email'],
                generate_password_hash(data['password'])
            )
        )

        mysql.connection.commit()

        cursor.close()

        session.pop('pending_registration', None)

        flash(
            'Citizen account created successfully. Please login.',
            'success'
        )

        return redirect(url_for('auth.login'))

    return render_template(
        'auth/verify_otp.html',
        email=data['email']
    )
# ======================================
# FORGOT PASSWORD
# ======================================

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        role = request.form['role']
        email = request.form['email']

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT user_id, full_name, role
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        # No account found
        if not user:

            flash('No account found with this email.', 'danger')

            return redirect(url_for('auth.forgot_password'))

        # Role mismatch
        if user[2] != role:

            flash(
                'The selected account type does not match this email address.',
                'danger'
            )

            return redirect(url_for('auth.forgot_password'))

        # Mayor cannot reset directly
        if role == 'mayor':

            flash(
                'Mayor password cannot be reset here. Please contact the Administrator.',
                'warning'
            )

            return redirect(url_for('auth.login'))

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Store reset data temporarily
        session['password_reset'] = {
            'user_id': user[0],
            'full_name': user[1],
            'email': email,
            'role': role,
            'otp': otp,
            'expiry': (
                datetime.now() + timedelta(minutes=5)
            ).isoformat()
        }

        # Send reset email
        msg = Message(
            subject='Digital Palika Password Reset Code',
            sender='gnawalishishir222@gmail.com',
            recipients=[email]
        )

        msg.body = f'''
Hello {user[1]},

You requested a password reset for your Digital Palika account.

Your verification code is:

{otp}

This code is valid for 5 minutes.

If you did not request this reset, please ignore this email.

Digital Palika
Smart Municipality Management System
'''

        mail.send(msg)

        flash(
            'Password reset verification code has been sent to your email.',
            'success'
        )

        return redirect(url_for('auth.verify_reset_otp'))

    return render_template('auth/forgot_password.html')

# ======================================
# VERIFY RESET OTP
# ======================================

@auth.route('/verify-reset-otp', methods=['GET', 'POST'])
def verify_reset_otp():

    data = session.get('password_reset')

    if not data:

        flash('Password reset session expired.', 'warning')

        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':

        entered_otp = request.form['otp']

        expiry = datetime.fromisoformat(data['expiry'])

        if datetime.now() > expiry:

            session.pop('password_reset', None)

            flash(
                'OTP has expired. Please request a new password reset.',
                'warning'
            )

            return redirect(url_for('auth.forgot_password'))

        if entered_otp != data['otp']:

            flash('Invalid verification code.', 'danger')

            return redirect(url_for('auth.verify_reset_otp'))

        return redirect(url_for('auth.reset_password'))

    return render_template(
        'auth/verify_reset_otp.html',
        email=data['email']
    )


# ======================================
# RESET PASSWORD
# ======================================

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    data = session.get('password_reset')

    if not data:

        flash('Password reset session expired.', 'warning')

        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check password match
        if password != confirm_password:

            flash('Passwords do not match.', 'danger')

            return redirect(url_for('auth.reset_password'))

        cursor = mysql.connection.cursor()

        # Get current password hash
        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE user_id=%s
            """,
            (data['user_id'],)
        )

        current_password_hash = cursor.fetchone()[0]

        # Prevent reusing the old password
        if check_password_hash(current_password_hash, password):

            cursor.close()

            flash(
                'You cannot use the password you are already using. Please choose a different password.',
                'warning'
            )

            return redirect(url_for('auth.reset_password'))

        # Hash the new password
        hashed_password = generate_password_hash(password)

        # Update password
        cursor.execute(
            """
            UPDATE users
            SET password=%s
            WHERE user_id=%s
            """,
            (hashed_password, data['user_id'])
        )

        mysql.connection.commit()

        cursor.close()

        # Clear reset session
        session.pop('password_reset', None)

        flash(
            'Password has been reset successfully. Please login.',
            'success'
        )

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')

# ======================================
# LOGOUT
# ======================================

@auth.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('auth.login'))