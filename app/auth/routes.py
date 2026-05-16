from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "user")

        if not name or not email or not password:
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This email is already registered. Please login or use another email.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            name=name,
            email=email,
            role=role,
            password_hash=generate_password_hash(password)
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash("User registered successfully. Please login.", "success")
            return redirect(url_for("auth.login"))

        except IntegrityError:
            db.session.rollback()
            flash("Registration failed because this email already exists.", "danger")
            return redirect(url_for("auth.register"))

        except Exception:
            db.session.rollback()
            flash("Something went wrong during registration. Please try again.", "danger")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))