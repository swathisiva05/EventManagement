from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash,
    session, g
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------
# App Config
# -------------------------------------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

db = SQLAlchemy(app)

# -------------------------------------------------
# Models
# -------------------------------------------------
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)


class Resource(db.Model):
    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(120), nullable=False)
    resource_type = db.Column(db.String(80), nullable=False)


class Allocation(db.Model):
    allocation_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id"))
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.resource_id"))

    event = db.relationship(Event)
    resource = db.relationship(Resource)


with app.app_context():
    db.create_all()

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.before_request
def load_user():
    uid = session.get("user_id")
    g.user = User.query.get(uid) if uid else None


def parse_dt(val):
    return datetime.strptime(val, "%Y-%m-%dT%H:%M")

# -------------------------------------------------
# HOME (WELCOME PAGE)
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -------------------------------------------------
# AUTH
# -------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for("signup"))

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Signup successful. Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"].lower()
        ).first()

        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.user_id
            return redirect(url_for("dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        total_events=Event.query.count(),
        total_resources=Resource.query.count(),
        total_allocations=Allocation.query.count(),
        upcoming_events=Event.query.order_by(Event.start_time).limit(5).all()
    )

# -------------------------------------------------
# EVENTS
# -------------------------------------------------
@app.route("/events")
@login_required
def list_events():
    return render_template(
        "events.html",
        events=Event.query.order_by(Event.start_time).all()
    )

@app.route("/events/new", methods=["GET", "POST"])
@app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def upsert_event(event_id=None):
    event = Event.query.get(event_id) if event_id else Event()

    if request.method == "POST":
        event.title = request.form["title"]
        event.start_time = parse_dt(request.form["start_time"])
        event.end_time = parse_dt(request.form["end_time"])
        event.description = request.form.get("description")

        if event.start_time >= event.end_time:
            flash("End time must be after start time")
            return render_template("event_form.html", event=event)

        db.session.add(event)
        db.session.commit()
        return redirect(url_for("list_events"))

    return render_template("event_form.html", event=event)

@app.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("list_events"))

# -------------------------------------------------
# RESOURCES
# -------------------------------------------------
@app.route("/resources")
@login_required
def list_resources():
    return render_template("resources.html", resources=Resource.query.all())

@app.route("/resources/new", methods=["GET", "POST"])
@login_required
def upsert_resource():
    if request.method == "POST":
        db.session.add(
            Resource(
                resource_name=request.form["resource_name"],
                resource_type=request.form["resource_type"]
            )
        )
        db.session.commit()
        return redirect(url_for("list_resources"))

    return render_template("resource_form.html")

# -------------------------------------------------
# ALLOCATIONS
# -------------------------------------------------
@app.route("/allocations")
@login_required
def list_allocations():
    return render_template("allocations.html", allocations=Allocation.query.all())

# -------------------------------------------------

@app.route("/allocations/new", methods=["GET", "POST"])
@login_required
def allocation_form():
    events = Event.query.all()
    resources = Resource.query.all()

    if request.method == "POST":
        alloc = Allocation(
            event_id=request.form["event_id"],
            resource_id=request.form["resource_id"]
        )
        db.session.add(alloc)
        db.session.commit()
        return redirect(url_for("list_allocations"))

    return render_template(
        "allocation_form.html",
        events=events,
        resources=resources
    )



# CONFLICTS
# -------------------------------------------------
@app.route("/conflicts")
@login_required
def conflicts():
    return render_template("conflicts.html", conflicts=[])

# -------------------------------------------------
# REPORT
# -------------------------------------------------
@app.route("/report")
@login_required
def report():
    return render_template("report.html", allocations=Allocation.query.all())

# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
