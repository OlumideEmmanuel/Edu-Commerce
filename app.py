from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS

# ---------------- Initialize App ---------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# ---------------- Initialize Extensions ---------------- #
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
CORS(app)  # Allow frontend (Vercel) to call backend (Render)

# ---------------- User Loader ---------------- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Database Models ---------------- #
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Course('{self.title}', {self.price})"

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

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- Signup Route ---------------- #
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", 'danger')
            return redirect(url_for('signup'))

        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose another.', 'warning')
            return redirect(url_for('signup'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))

        # Hash password and create new user
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template("signup.html")

# ---------------- Login Route ---------------- #
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("You don't have an account. Please sign up.", 'danger')
            return redirect(url_for('signup'))

        if not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template("login.html")

# ---------------- Dashboard Route ---------------- #
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)

# ---------------- Logout Route ---------------- #
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ---------------- API Routes ---------------- #
@app.route("/api/courses")
def api_courses():
    courses = Course.query.all()
    return jsonify([{"id": c.id, "title": c.title, "price": c.price} for c in courses])

@app.route("/api/user")
@login_required
def api_user():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    })

# ---------------- Run App ---------------- #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensures DB tables exist
    app.run(debug=True)
