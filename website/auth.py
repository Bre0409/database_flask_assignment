from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from datetime import datetime
import os

auth = Blueprint("auth", __name__)

# --- SIGN UP ---
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    try:
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            first_name = request.form.get("firstName", "").strip()
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            # Validate inputs
            if not email or not first_name or not password1 or not password2:
                flash("All fields are required.", category="error")
                return redirect(url_for("auth.sign_up"))

            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email is already registered. Please log in.", category="error")
                return redirect(url_for("auth.login"))

            # Check password match
            if password1 != password2:
                flash("Passwords do not match.", category="error")
                return redirect(url_for("auth.sign_up"))

            # Hash password
            hashed_pw = generate_password_hash(password1, method="pbkdf2:sha256")

            # Create new user
            new_user = User(
                email=email,
                first_name=first_name,
                password=hashed_pw,
                created_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully! Please log in.", category="success")
            return redirect(url_for("auth.login"))

        return render_template("sign_up.html")

    except Exception as e:
        # Print the error in the terminal for debugging
        print("Error during sign-up:", e)
        # show a flash message
        flash("An unexpected error occurred. Please try again.", category="error")
        return redirect(url_for("auth.sign_up"))


# --- LOGIN ---
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Store session values
            session["user_id"] = user.id
            session["user_email"] = user.email
            session["first_name"] = user.first_name
            flash(f"Welcome back, {user.first_name}!", category="success")
            return redirect(url_for("views.home"))
        else:
            flash("Invalid email or password.", category="error")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# --- LOGOUT ---
@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", category="info")
    return redirect(url_for("auth.login"))
