from datetime import datetime
from zoneinfo import ZoneInfo
from . import db

# ✅ Local timezone
LOCAL_TZ = ZoneInfo("Europe/London")


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(LOCAL_TZ))

    # ✅ Relationships
    tasks = db.relationship(
        "Task", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    events = db.relationship(
        "Event", backref="user", lazy=True, cascade="all, delete-orphan"
    )


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(LOCAL_TZ))

    # ✅ Due date for daily/weekly/monthly schedules
    due_date = db.Column(db.Date, nullable=False, index=True)

    # ✅ Optional specific time (only clock time, not full datetime)
    time = db.Column(db.Time, nullable=True, index=True)

    # ✅ Link to User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # ✅ Date + Time for scheduling
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(LOCAL_TZ))

    # ✅ Link to User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
