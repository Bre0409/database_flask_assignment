from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from . import db
from .models import Event, Task
from .utils import login_required_db

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET', 'POST'])
@login_required_db
def add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')

        if not title or not date_str:
            flash("Title and date are required", category="error")
            return redirect(url_for("events.add_event"))

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format", category="error")
            return redirect(url_for("events.add_event"))

        new_event = Event(
            title=title,
            description=description,
            date=date,
            user_id=session["user_id"]
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event added successfully!", category="success")
        return redirect(url_for("events.add_event"))

    events = Event.query.filter_by(user_id=session["user_id"]).order_by(Event.date).all()
    return render_template('events.html', events=events, edit_event=None)


@events_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required_db
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id == session["user_id"]:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted.", category="info")
    return redirect(url_for('events.add_event'))


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

        try:
            event.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format", category="error")

        db.session.commit()
        flash("Event updated successfully!", category="success")
        return redirect(url_for('events.add_event'))

    events = Event.query.filter_by(user_id=session["user_id"]).all()
    return render_template('events.html', events=events, edit_event=event)


@events_bp.route('/calendar')
@login_required_db
def calendar():
    # Fetch both Events and Tasks
    events = Event.query.filter_by(user_id=session["user_id"]).all()
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()

    # Merge into a single list for calendar display
    calendar_items = []
    for e in events:
        calendar_items.append({
            "title": e.title,
            "description": e.description,
            "date": e.date.isoformat(),
            "type": "event"
        })

    for t in tasks:
        calendar_items.append({
            "title": t.text,
            "description": "Task" + (" (completed)" if t.completed else ""),
            "date": t.due_date.isoformat(),
            "type": "task"
        })

    return render_template('calendar.html', events=calendar_items)
