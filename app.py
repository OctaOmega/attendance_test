from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from model import Attendee, db


def create_app():
    app = Flask(__name__)

    base_directory = Path(__file__).resolve().parent
    database_path = base_directory / "attendance.db"

    app.config["SECRET_KEY"] = "replace-with-a-secure-secret-key"
    #DB
    #app.config["SQLALCHEMY_DATABASE_URI"] = (f"mysql+pymysql://root:mysql@localhost:3306/attendance_db")
    app.config["SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{database_path.as_posix()}")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app


def register_routes(app):
    @app.route("/")
    def index():
        search_term = request.args.get("search", "").strip()

        query = Attendee.query

        if search_term:
            search_pattern = f"%{search_term}%"

            query = query.filter(
                or_(
                    Attendee.name.ilike(search_pattern),
                    Attendee.email.ilike(search_pattern),
                    Attendee.department.ilike(search_pattern),
                    Attendee.attendance_status.ilike(search_pattern),
                )
            )

        attendees = query.order_by(Attendee.created_at.desc()).all()

        all_attendees = Attendee.query.all()

        total_responses = len(all_attendees)

        attending_employees = sum(
            1
            for attendee in all_attendees
            if attendee.attendance_status == "Attending"
        )

        total_people_attending = sum(
            1 + attendee.guest_count
            for attendee in all_attendees
            if attendee.attendance_status == "Attending"
        )

        return render_template(
            "index.html",
            attendees=attendees,
            search_term=search_term,
            total_responses=total_responses,
            attending_employees=attending_employees,
            total_people_attending=total_people_attending,
        )

    @app.route("/attendees/add", methods=["POST"])
    def add_attendee():
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        attendance_status = request.form.get(
            "attendance_status",
            "",
        ).strip()
        dietary_requirements = request.form.get(
            "dietary_requirements",
            "",
        ).strip()

        try:
            guest_count = int(request.form.get("guest_count", 0))
        except ValueError:
            guest_count = 0

        guest_count = max(guest_count, 0)

        valid_statuses = {
            "Attending",
            "Not attending",
            "Maybe",
        }

        if not name or not email:
            flash("Name and email are required.", "error")
            return redirect(url_for("index"))

        if attendance_status not in valid_statuses:
            flash("Select a valid attendance status.", "error")
            return redirect(url_for("index"))

        if attendance_status != "Attending":
            guest_count = 0

        attendee = Attendee(
            name=name,
            email=email,
            department=department or None,
            attendance_status=attendance_status,
            guest_count=guest_count,
            dietary_requirements=dietary_requirements or None,
        )

        try:
            db.session.add(attendee)
            db.session.commit()
            flash("Attendance response saved.", "success")
        except Exception:
            db.session.rollback()
            flash("The attendance response could not be saved.", "error")

        return redirect(url_for("index"))

    @app.route(
        "/attendees/<int:attendee_id>/delete",
        methods=["POST"],
    )
    def delete_attendee(attendee_id):
        attendee = db.session.get(Attendee, attendee_id)

        if attendee is None:
            flash("Attendance record not found.", "error")
            return redirect(url_for("index"))

        try:
            db.session.delete(attendee)
            db.session.commit()
            flash("Attendance record deleted.", "success")
        except Exception:
            db.session.rollback()
            flash("The attendance record could not be deleted.", "error")

        return redirect(url_for("index"))


app = create_app()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)