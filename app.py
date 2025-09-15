from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"  # change in production

# ---------------- DATABASE SETUP ---------------- #
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------------- USER MODEL ---------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# ---------------- Routes ---------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/coursedetails")
def coursedetails():
    return render_template("coursedetails.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Here you can process the message (save to DB, send email, etc.)
        # For now, we'll just flash a success message
        flash(f"✅ Thank you {name}, your message has been sent!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------- SIGNUP ---------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check if username/email already exists
        if User.query.filter_by(username=username).first():
            flash("❌ Username already taken. Please log in.", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("❌ Email already registered. Please log in.", "danger")
            return redirect(url_for("signup"))

        # Check password
        if password != confirm_password:
            flash("❌ Passwords do not match.", "danger")
            return redirect(url_for("signup"))

        if len(password) < 6:
            flash("❌ Password must be at least 6 characters.", "danger")
            return redirect(url_for("signup"))

        # Create user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Sign up successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------- LOGIN ---------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("❌ You don’t have an account. Please sign up.", "danger")
            return redirect(url_for("signup"))

        if check_password_hash(user.password, password):
            session["user"] = user.username
            flash(f"✅ Welcome, {user.username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Incorrect password. Try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


# ---------- DASHBOARD ---------- #
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    else:
        flash("⚠️ You must log in first.", "warning")
        return redirect(url_for("login"))


# ---------- LOGOUT ---------- #
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("👋 You have been logged out.", "info")
    return redirect(url_for("login"))


# ---------- EXTRA PAGES PLACEHOLDER ---------- #
# @app.route("/courses")
# def courses():
#     return "<h1>Courses Page</h1>"

# @app.route("/services")
# def services():
#     return "<h1>Services Page</h1>"

# @app.route("/about")
# def about():
#     return "<h1>About Us Page</h1>"

# @app.route("/contact")
# def contact():
#     return "<h1>Contact Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)
