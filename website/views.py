# website/views.py
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
    Convert a day label ('Today', 'Tomorrow', 'Wednesday', etc.) into
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
                days_ahead = 7  # ensure we mean *next* week, not today
            return today + timedelta(days=days_ahead)

    return today


# ---------------- Home ----------------
@views.route("/")
def home():
    return render_template("home.html")


# ---------------- Daily Organiser ----------------
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
                created_at=datetime.now(LOCAL_TZ),
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
        get_date_for_day=get_date_for_day,
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


# ---------------- Daily Schedule ----------------
@views.route("/schedule/daily")
def schedule_daily():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    tasks = Task.query.filter_by(user_id=session["user_id"], due_date=today).all()

    return render_template("schedule_daily.html", tasks=tasks)


# ---------------- Weekly Schedule ----------------
@views.route("/schedule/weekly")
def schedule_weekly():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    start_week = today - timedelta(days=today.weekday())  # Monday
    end_week = start_week + timedelta(days=6)

    all_tasks = Task.query.filter(
        Task.user_id == session["user_id"],
        Task.due_date >= start_week,
        Task.due_date <= end_week,
    ).order_by(Task.due_date.asc()).all()

    # Group tasks by date
    weekly_tasks = {}
    for task in all_tasks:
        weekly_tasks.setdefault(task.due_date, []).append(task)

    return render_template("schedule_weekly.html", weekly_tasks=weekly_tasks)


# ---------------- Monthly Schedule ----------------
@views.route("/schedule/monthly")
def schedule_monthly():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    start_month = today.replace(day=1)

    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    end_month = next_month - timedelta(days=1)

    all_tasks = Task.query.filter(
        Task.user_id == session["user_id"],
        Task.due_date >= start_month,
        Task.due_date <= end_month,
    ).order_by(Task.due_date.asc()).all()

    # Group tasks by date
    monthly_tasks = {}
    for task in all_tasks:
        monthly_tasks.setdefault(task.due_date, []).append(task)

    return render_template("schedule_monthly.html", monthly_tasks=monthly_tasks)
