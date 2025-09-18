from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Task, Event
from . import db
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from collections import defaultdict

views = Blueprint("views", __name__)

LOCAL_TZ = ZoneInfo("Europe/London")  

# ---------------- Helper ----------------
def get_date_for_day(day_name: str) -> date:
    today = datetime.now(LOCAL_TZ).date()
    if day_name == "Today":
        return today
    elif day_name == "Tomorrow":
        return today + timedelta(days=1)
    else:
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_name in weekdays:
            today_index = today.weekday()
            target_index = weekdays.index(day_name)
            days_ahead = (target_index - today_index) % 7
            if days_ahead == 0:
                days_ahead = 7
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
    selected_day = request.args.get("day", "Today")
    selected_date = get_date_for_day(selected_day)

    if request.method == "POST":
        task_text = request.form.get("task")
        task_time_str = request.form.get("task_time")
        task_time = None
        if task_time_str:
            try:
                task_time = datetime.strptime(task_time_str, "%H:%M").time()
            except ValueError:
                flash("Invalid time format. Use HH:MM.", "warning")

        if task_text:
            new_task = Task(
                text=task_text,
                due_date=selected_date,
                user_id=user_id,
                time=task_time,
                created_at=datetime.now(LOCAL_TZ),
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        return redirect(url_for("views.task_list", day=selected_day))

    tasks = Task.query.filter_by(user_id=user_id, due_date=selected_date)\
        .order_by(Task.time.asc().nullslast()).all()

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
    edited_time_str = request.form.get("edited_time")
    if edited_time_str:
        try:
            task.time = datetime.strptime(edited_time_str, "%H:%M").time()
        except ValueError:
            flash("Invalid time format. Use HH:MM.", "warning")
    else:
        task.time = None
    db.session.commit()
    flash("Task updated successfully!", "success")
    return redirect(url_for("views.task_list", day=request.args.get("day", "Today")))

# ---------------- Schedules Page ----------------
@views.route("/schedules")
def schedules():
    if "user_id" not in session:
        flash("Please log in to view schedules.", "warning")
        return redirect(url_for("auth.login"))
    return render_template("schedules.html")

# ---------------- Daily Schedule ----------------
@views.route("/schedule/daily")
def schedule_daily():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    tasks = Task.query.filter_by(user_id=session["user_id"], due_date=today).all()
    events = Event.query.filter_by(user_id=session["user_id"], date=today).all()

    daily_items = sorted(tasks + events, key=lambda x: (getattr(x, 'time', None) or datetime.min.time()))

    return render_template("schedule_daily.html", daily_items=daily_items, current_date=today)

# ---------------- Weekly Schedule ----------------
@views.route("/schedule/weekly")
def schedule_weekly():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)

    tasks = Task.query.filter(Task.user_id==session["user_id"], Task.due_date>=start_week, Task.due_date<=end_week).all()
    events = Event.query.filter(Event.user_id==session["user_id"], Event.date>=start_week, Event.date<=end_week).all()

    weekly_items = defaultdict(list)
    for t in tasks: weekly_items[t.due_date].append(t)
    for e in events: weekly_items[e.date].append(e)

    for day in weekly_items:
        weekly_items[day].sort(key=lambda x: x.time if x.time else datetime.min.time())
    weekly_items = dict(sorted(weekly_items.items()))

    return render_template("schedule_weekly.html", weekly_items=weekly_items, current_date=start_week)

# ---------------- Monthly Schedule ----------------
@views.route("/schedule/monthly")
def schedule_monthly():
    if "user_id" not in session:
        flash("Please log in to view your schedule.", "warning")
        return redirect(url_for("auth.login"))

    today = datetime.now(LOCAL_TZ).date()
    start_month = today.replace(day=1)
    next_month = today.replace(year=today.year + (today.month // 12), month=(today.month % 12) + 1, day=1)
    end_month = next_month - timedelta(days=1)

    tasks = Task.query.filter(Task.user_id==session["user_id"], Task.due_date>=start_month, Task.due_date<=end_month).all()
    events = Event.query.filter(Event.user_id==session["user_id"], Event.date>=start_month, Event.date<=end_month).all()

    monthly_items = defaultdict(list)
    for t in tasks: monthly_items[t.due_date].append(t)
    for e in events: monthly_items[e.date].append(e)

    for day in monthly_items:
        monthly_items[day].sort(key=lambda x: x.time if x.time else datetime.min.time())
    monthly_items = dict(sorted(monthly_items.items()))

    return render_template("schedule_monthly.html", monthly_items=monthly_items, current_date=today)
