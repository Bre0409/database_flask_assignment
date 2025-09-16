from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from website import db
from website.models import Event, Task
from website.utils import login_required_db

events_bp = Blueprint("events", __name__)

# ---------------- Add Event ----------------
@events_bp.route('/events', methods=['GET', 'POST'])
@login_required_db
def add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        time_str = request.form.get('time')

        if not title or not date_str:
            flash("Title and date are required", category="error")
            return redirect(url_for("events.add_event"))

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format", category="error")
            return redirect(url_for("events.add_event"))

        event_time = None
        if time_str:
            try:
                event_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                flash("Invalid time format", category="error")
                return redirect(url_for("events.add_event"))

        new_event = Event(
            title=title,
            description=description,
            date=date,
            time=event_time,
            user_id=session["user_id"]
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event added successfully!", category="success")
        return redirect(url_for("events.add_event"))

    events = Event.query.filter_by(user_id=session["user_id"])\
        .order_by(Event.date.asc(), Event.time.asc().nullsfirst()).all()
    return render_template('events.html', events=events, edit_event=None)

# ---------------- Delete Event ----------------
@events_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required_db
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id == session["user_id"]:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted.", category="info")
    return redirect(url_for('events.add_event'))

# ---------------- Edit Event ----------------
@events_bp.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required_db
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != session["user_id"]:
        return redirect(url_for('events.add_event'))

    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        date_str = request.form.get('date')
        time_str = request.form.get('time')

        try:
            event.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format", category="error")

        if time_str:
            try:
                event.time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                flash("Invalid time format", category="error")
        else:
            event.time = None

        db.session.commit()
        flash("Event updated successfully!", category="success")
        return redirect(url_for('events.add_event'))

    events = Event.query.filter_by(user_id=session["user_id"])\
        .order_by(Event.date.asc(), Event.time.asc().nullsfirst()).all()
    return render_template('events.html', events=events, edit_event=event)

# ---------------- Calendar ----------------
@events_bp.route('/calendar')
@login_required_db
def calendar():
    events = Event.query.filter_by(user_id=session["user_id"])\
        .order_by(Event.date.asc(), Event.time.asc().nullsfirst()).all()
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()

    calendar_items = []
    for e in events:
        calendar_items.append({
            "title": e.title,
            "description": e.description,
            "date": e.date.isoformat(),
            "time": e.time.strftime("%H:%M") if e.time else None,
            "type": "event"
        })
    for t in tasks:
        calendar_items.append({
            "title": t.text,
            "description": "Task" + (" (completed)" if t.completed else ""),
            "date": t.due_date.isoformat(),
            "time": t.time.strftime("%H:%M") if t.time else None,
            "type": "task"
        })

    return render_template('calendar.html', events=calendar_items)

