from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from models import Employee, Admin
from flask_login import login_user, logout_user, login_required

@app.route("/")
def home():
    return render_template("employee_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]
        department = request.form["department"]
        unit = request.form["unit"]
        location = request.form["location"]
        feedback = request.form["feedback"]
        
        new_employee = Employee(name=name, phone=phone, address=address, 
                                department=department, unit=unit, 
                                location=location, feedback=feedback)
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee Data Submitted!", "success")
        return redirect(url_for("home"))

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Credentials!", "danger")
    
    return render_template("admin_login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    employees = Employee.query.all()
    return render_template("admin_dashboard.html", employees=employees)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin_login"))
