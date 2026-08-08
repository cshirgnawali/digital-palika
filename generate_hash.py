from werkzeug.security import generate_password_hash

passwords = {
    "admin123": "Admin",
    "mayor123": "Mayor",
    "staff123": "Staff",
    "citizen123": "Citizen"
}

for password, role in passwords.items():
    print(f"{role}:")
    print(generate_password_hash(password))
    print()