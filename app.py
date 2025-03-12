from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Connect to your remote MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql7767154:gukxfaZppt@sql7.freesqldatabase.com:3306/sql7767154'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    devices = db.Column(db.Text, default='[]')

    def add_device(self, name, ip):
        device_list = json.loads(self.devices)
        device_list.append({'name': name, 'ip': ip})
        self.devices = json.dumps(device_list)
        db.session.commit()

    def remove_device(self, name):
        device_list = json.loads(self.devices)
        device_list = [device for device in device_list if device['name'] != name]
        self.devices = json.dumps(device_list)
        db.session.commit()


# Load user function
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Route: Home (requires login)
@app.route('/')
@login_required
def home():
    user = current_user
    devices = json.loads(user.devices)
    return render_template('home.html', username=user.username, devices=devices)


# Route: Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Choose another one.')
            return redirect(url_for('register'))

        # Hash the password before saving using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


# Route: Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Route: Add Device
@app.route('/add_device', methods=['POST'])
@login_required
def add_device():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Ensure the user is logged in

    device_name = request.form['device_name']
    device_ip = request.form['device_ip']
    current_user.add_device(device_name, device_ip)

    return redirect(url_for('home'))  # Redirect to home after adding device


# Route: Remove Device
@app.route('/remove_device', methods=['POST'])
@login_required
def remove_device():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Ensure the user is logged in

    device_name = request.form['device_name']
    current_user.remove_device(device_name)

    return redirect(url_for('home'))  # Redirect to home after removing device


# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database tables in MySQL
    app.run(host="0.0.0.0", port=5000, debug=True)
