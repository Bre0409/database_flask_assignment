from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Task
from . import db
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo

views = Blueprint("views", __name__)

# ✅ Use Europe/London timezone everywhere
LOCAL_TZ = ZoneInfo("Europe/London")


def get_date_for_day(day_name: str) -> date:
    """
    Convert a day label ('Today', 'Tomorrow', 'Monday', etc.) into
    an actual date in Europe/London timezone.
    """
    today = datetime.now(LOCAL_TZ).date()

    if day_name == "Today":
        return today
    elif day_name == "Tomorrow":
        return today + timedelta(days=1)
    else:
        weekdays = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ]
        if day_name in weekdays:
            today_index = today.weekday()  # Monday=0, Sunday=6
            target_index = weekdays.index(day_name)
            days_ahead = (target_index - today_index) % 7
            if days_ahead == 0:
                days_ahead = 7  # ensure *next* week, not today
            return today + timedelta(days=days_ahead)

    return today


@views.route("/")
def home():
    return render_template("home.html")  # ✅ make sure you have templates/home.html


@views.route("/tasks", methods=["GET", "POST"])
def task_list():
    if "user_id" not in session:
        flash("Please log in to view your tasks.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Selected day from query params (default "Today")
    selected_day = request.args.get("day", "Today")
    selected_date = get_date_for_day(selected_day)

    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            new_task = Task(
                text=task_text,
                due_date=selected_date,
                user_id=user_id,
                created_at=datetime.now(LOCAL_TZ),  # ✅ timezone-aware
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        return redirect(url_for("views.task_list", day=selected_day))

    tasks = (
        Task.query.filter_by(user_id=user_id, due_date=selected_date)
        .order_by(Task.created_at.desc())
        .all()
    )

    weekdays = ["Today", "Tomorrow", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return render_template(
        "daily_organiser.html",
        tasks=tasks,
        selected_day=selected_day,
        weekdays=weekdays,
        selected_date=selected_date,
        get_date_for_day=get_date_for_day,  # ✅ pass helper
        Task=Task,                          # ✅ allow queries in template
    )


@views.route("/tasks/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get("user_id"):
        flash("Unauthorized action.", "danger")
        return redirect(url_for("views.task_list"))

    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("views.task_list", day=request.args.get("day", "Today")))


@views.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get("user_id"):
        flash("Unauthorized action.", "danger")
        return redirect(url_for("views.task_list"))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.task_list", day=request.args.get("day", "Today")))


@views.route("/tasks/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get("user_id"):
        flash("Unauthorized action.", "danger")
        return redirect(url_for("views.task_list"))

    new_text = request.form.get("edited_text")
    if new_text:
        task.text = new_text
        db.session.commit()
        flash("Task updated successfully!", "success")

    return redirect(url_for("views.task_list", day=request.args.get("day", "Today")))
