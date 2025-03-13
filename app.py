import json
import os
import random

import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

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
    settings = db.Column(db.Text, default='{}')

    def add_device(self, name, ip, type):
        device_list = json.loads(self.devices)
        device_list.append({'name': name, 'ip': ip, 'type': type})
        self.devices = json.dumps(device_list)
        db.session.commit()

    def remove_device(self, name):
        device_list = json.loads(self.devices)
        device_list = [device for device in device_list if device['name'] != name]
        self.devices = json.dumps(device_list)
        db.session.commit()

    def get_devices(self):
        return json.loads(self.devices)

    #     save user settings: theme, show ip address
    def save_settings(self, user_settings):
        self.settings = json.dumps(user_settings)
        db.session.commit()

    def get_settings(self):
        return json.loads(self.settings)


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
    return render_template('home.html', username=user.username, devices=devices, get_device_icon=get_device_icon)


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
    device_type = request.form['device_type']
    current_user.add_device(device_name, device_ip, device_type)

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


@app.route('/toggle_device', methods=['POST'])
def toggle_device():
    data = request.get_json()
    device_name = data.get('device_name')
    device_ip = data.get('device_ip')
    state = data.get('state')

    print(f"Turning {state} the device: {device_name}, IP: {device_ip}")

    return jsonify({'message': f'Toggling device: {device_name}, IP: {device_ip}, State: {state}'}), 200


@app.route('/save_settings', methods=['POST'])
@login_required
def save_settings():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    current_user.save_settings(data)
    return jsonify({'status': 'success', 'message': 'Settings saved successfully'})


@app.route('/get_settings', methods=['GET'])
@login_required
def get_settings():
    return jsonify(current_user.get_settings())


def get_device_icon(device_type):
    icons = {
        "light": "fa-lightbulb",
        "fan": "fa-fan",
        "thermostat": "fa-thermometer-half",
        "plug": "fa-plug",
        "sensor": "fa-rss",
        "fronius": "fa-solar-panel"
    }
    return icons.get(device_type, "fa-question-circle")  # Default icon if type not found


@app.route('/solar-data')
def solar_data():
    devices = fetch_fronius_device_data()
    if isinstance(devices, list) and devices:
        device = devices[0]
        data = device.get('data', {})

        if isinstance(data, dict):
            power = data.get('Body', {}).get('Data', {}).get('PowerReal_P_Sum', 0)
            energy_produced = data.get('Body', {}).get('Data', {}).get('EnergyReal_WAC_Sum_Produced', 0)
            energy_consumed = data.get('Body', {}).get('Data', {}).get('EnergyReal_WAC_Sum_Consumed', 0)
            net_energy_balance = energy_produced - energy_consumed
            self_sufficiency = round((energy_produced / max(energy_consumed, 1)) * 100, 2)

            grid_import = data.get('Body', {}).get('Data', {}).get('EnergyReal_WAC_Plus_Absolute', 0)
            grid_export = data.get('Body', {}).get('Data', {}).get('EnergyReal_WAC_Minus_Absolute', 0)

            voltage_phase_1 = data.get('Body', {}).get('Data', {}).get('Voltage_AC_Phase_1', 0)
            voltage_phase_2 = data.get('Body', {}).get('Data', {}).get('Voltage_AC_Phase_2', 0)
            voltage_phase_3 = data.get('Body', {}).get('Data', {}).get('Voltage_AC_Phase_3', 0)

            current_phase_1 = data.get('Body', {}).get('Data', {}).get('Current_AC_Phase_1', 0)
            current_phase_2 = data.get('Body', {}).get('Data', {}).get('Current_AC_Phase_2', 0)
            current_phase_3 = data.get('Body', {}).get('Data', {}).get('Current_AC_Phase_3', 0)

            power_factor = data.get('Body', {}).get('Data', {}).get('PowerFactor_Sum', 0)
            reactive_power = data.get('Body', {}).get('Data', {}).get('PowerReactive_Q_Sum', 0)

            co2_savings = 10.82  # You might want to calculate this dynamically

            return jsonify({
                'power': power,
                'energy_produced': energy_produced,
                'energy_consumed': energy_consumed,
                'net_energy_balance': net_energy_balance,
                'self_sufficiency': self_sufficiency,
                'grid_import': grid_import,
                'grid_export': grid_export,
                'voltage_phase_1': voltage_phase_1,
                'voltage_phase_2': voltage_phase_2,
                'voltage_phase_3': voltage_phase_3,
                'current_phase_1': current_phase_1,
                'current_phase_2': current_phase_2,
                'current_phase_3': current_phase_3,
                'power_factor': power_factor,
                'reactive_power': reactive_power,
                'co2_savings': co2_savings
            })
    return jsonify({'error': 'No data available'})


def fetch_fronius_device_data():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Ensure the user is logged in

    device_data = []
    for device in current_user.get_devices():
        if device['type'].lower() == 'fronius':
            data = fetch_fronius_data(device['ip'])
            if data:
                device_data.append({'name': device['name'], 'data': data})
    return device_data


def fetch_fronius_data(ip_address):
    url = f'http://{ip_address}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=0&DataCollection=CommonInverterData'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()  # Return parsed JSON data
    except requests.RequestException as e:
        print(f"Error fetching data from {ip_address}: {e}")
        return None


@app.route('/temperature-data', methods=['GET'])
def get_temperature_data():
    temperature = round(random.uniform(5, 40.0), 2)  # Simulated temperature in °C
    humidity = round(random.uniform(0, 70.0), 2)  # Simulated humidity in %
    data = {
        'temperature': temperature,
        'humidity': humidity
    }
    return jsonify(data)


# Main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database tables in MySQL
    app.run(host="0.0.0.0", port=5000, debug=True)
