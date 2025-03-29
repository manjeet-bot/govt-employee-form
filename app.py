from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from config import DATABASE_URL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for security

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Employee Form Page
@app.route("/", methods=["GET", "POST", "HEAD"])
def employee_form():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        family = request.form["family"]
        address = request.form["address"]
        department = request.form["department"]
        photo = request.form["photo"]
        unit = request.form["unit"]
        location = request.form["location"]
        feedback = request.form["feedback"]

        cur.execute("INSERT INTO employees (name, phone, family, address, department, photo, unit, location, feedback) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, phone, family, address, department, photo, unit, location, feedback))
        conn.commit()
        return "Form Submitted Successfully!"
    
    return render_template("employee_form.html")

# Admin Login Page
@app.route("/admin", methods=["GET", "POST", "HEAD"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "password123":  # Change credentials
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_login.html")

# Admin Dashboard
@app.route("/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    return render_template("admin_dashboard.html", employees=employees)

# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True)
