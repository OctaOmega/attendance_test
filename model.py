from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Attendee(db.Model):
    __tablename__ = "attendees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100))
    attendance_status = db.Column(db.String(30), nullable=False)
    guest_count = db.Column(db.Integer, nullable=False, default=0)
    dietary_requirements = db.Column(db.String(250))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def __repr__(self):
        return f"<Attendee {self.name}>"