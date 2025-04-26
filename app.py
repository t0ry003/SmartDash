import os
import random
import requests
import setup
import base64
import platform
import subprocess
from setup import *
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

if not setup.check_config_file():
    print(f"{BColors.OKCYAN}Config file not found! Creating a new one...{BColors.ENDC}")
    db_uri = setup.create_config_file()
else:
    config = setup.load_config()
    db_uri = config["db_uri"] if config else None

if db_uri:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    print(f"{BColors.WARNING}No valid database configuration found. Exiting...{BColors.ENDC}")
    exit(1)

print(f"{BColors.OKGREEN}DB URI: {db_uri}{BColors.ENDC}")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    devices = db.Column(db.Text, default='[]')
    settings = db.Column(db.Text, default='{"theme": "dark", "show_ip": false}')
    profile_picture = db.Column(db.Text, default=None)

    def change_password(self, new_password):
        self.password = new_password
        db.session.commit()

    def add_device(self, name, ip, device_type):
        device_list = json.loads(self.devices)

        if device_type == 'thermostat' and any(device['type'] == 'thermostat' for device in device_list):
            raise ValueError("You can only add one thermostat.")

        device_list.append({'name': name, 'ip': ip, 'type': device_type})
        self.devices = json.dumps(device_list)
        db.session.commit()

    def remove_device(self, name):
        device_list = json.loads(self.devices)
        device_list = [device for device in device_list if device['name'] != name]
        self.devices = json.dumps(device_list)
        db.session.commit()

    def get_devices(self):
        return json.loads(self.devices)

    def save_settings(self, user_settings):
        self.settings = json.dumps(user_settings)
        db.session.commit()

    def get_settings(self):
        return json.loads(self.settings)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
@login_required
def home():
    user = current_user
    devices = json.loads(user.devices)
    return render_template('home.html', username=user.username, devices=devices, get_device_icon=get_device_icon)


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

        if User.query.count() == 0:
            role = 'admin'
        else:
            role = 'user'

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Registration successful! Your account {username} in as an {role}.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if not bcrypt.check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect.')
        return redirect(url_for('home'))

    if new_password != confirm_password:
        flash('New passwords do not match.')
        return redirect(url_for('home'))

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    current_user.change_password(hashed_password)
    flash('Password changed successfully. Please log in with your new password.')
    logout_user()
    return redirect(url_for('login'))


@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file uploaded.')
        return redirect(url_for('home'))

    file = request.files['profile_picture']
    if file.filename == '':
        flash('No selected file.')
        return redirect(url_for('home'))

    current_user.profile_picture = base64.b64encode(file.read()).decode('utf-8')
    db.session.commit()
    flash('Profile picture updated successfully.')
    return redirect(url_for('home'))


@app.route('/remove_profile_picture', methods=['POST'])
@login_required
def remove_profile_picture():
    current_user.profile_picture = None
    db.session.commit()
    flash('Profile picture removed successfully.')
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)

        if action == 'delete':
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.username} has been deleted.')
        elif action == 'change_role':
            new_role = request.form.get('new_role')
            if user.role == 'admin' and new_role == 'user':
                admin_count = User.query.filter_by(role='admin').count()
                if admin_count <= 1:
                    flash('Cannot change the role of the last remaining admin.')
                else:
                    user.role = new_role
                    db.session.commit()
                    flash(f'User {user.username} role has been changed to {new_role}.')
            else:
                user.role = new_role
                db.session.commit()
                flash(f'User {user.username} role has been changed to {new_role}.')

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


@app.route('/admin/update_settings/<int:user_id>', methods=['POST'])
@login_required
def admin_update_settings(user_id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    user.save_settings(data)
    return jsonify({'status': 'success', 'message': 'Settings updated successfully'})


@app.route('/admin/update_devices/<int:user_id>', methods=['POST'])
@login_required
def admin_update_devices(user_id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    devices = request.get_json()
    if not devices:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    user.devices = json.dumps(devices)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Devices updated successfully'})


@app.route('/save_devices/<int:user_id>', methods=['POST'])
@login_required
def save_devices(user_id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    devices = request.json
    user.devices = json.dumps(devices)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Devices saved successfully'})


@app.route('/delete_device/<int:user_id>/<int:device_id>', methods=['POST'])
@login_required
def delete_device(user_id, device_id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    devices = json.loads(user.devices)
    if device_id < len(devices):
        devices.pop(device_id)
        user.devices = json.dumps(devices)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Device deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Device not found'}), 404


@app.route('/add_device', methods=['POST'])
@login_required
def add_device():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    device_name = request.form['device_name']
    device_ip = request.form['device_ip']
    device_type = request.form['device_type']

    try:
        current_user.add_device(device_name, device_ip, device_type)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route('/export_data', methods=['GET'])
@login_required
def export_data():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if (current_user.role != 'admin'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    users = User.query.all()
    data = []

    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'devices': json.loads(user.devices),
            'settings': json.loads(user.settings)
        }
        data.append(user_data)

    response = jsonify(data)
    response.headers['Content-Disposition'] = 'attachment; filename=exported_data.json'
    return response


@app.route('/remove_device', methods=['POST'])
@login_required
def remove_device():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    device_name = request.form['device_name']
    current_user.remove_device(device_name)

    return redirect(url_for('home'))


@app.route('/toggle_device', methods=['POST'])
def toggle_device():
    data = request.get_json()
    device_name = data.get('device_name')
    device_ip = data.get('device_ip')
    device_type = data.get('device_type')
    state = data.get('state')

    print(
        f"{current_user.username} - Turning {state} the device: {device_name}, IP: {device_ip}, Device Type: {device_type}")

    return jsonify({'message': f'Toggling device: {device_name}, IP: {device_ip}, State: {state}'}), 200


@app.route('/get_status', methods=['GET'])
def get_status():
    data = request.get_json()
    device_name = data.get('device_name')
    device_ip = data.get('device_ip')
    device_type = data.get('device_type')

    response = os.system(f"ping -c 1 {device_ip}")
    if response == 0:
        status = "online"
    else:
        status = "offline"
    print(f"{current_user.username} - Device {device_name} is {status}")


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
    return icons.get(device_type, "fa-question-circle")


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

            co2_savings = 10.82

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
        return redirect(url_for('login'))

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
    thermostat_ip = None
    sensor_data = {
        'temperature': None,
        'humidity': None,
        'pressure': None,
        'thermostat_ip': None
    }

    if current_user.is_authenticated:
        devices = current_user.get_devices()
        thermostat = next((device for device in devices if device['type'] == 'thermostat'), None)
        if thermostat:
            thermostat_ip = thermostat['ip']
            sensor_data['thermostat_ip'] = thermostat_ip

            # Fetch data from the ESP32
            try:
                response = requests.get(f"http://{thermostat_ip}/sensor-data", timeout=5)
                if response.status_code == 200:
                    esp_data = response.json()
                    sensor_data.update({
                        'temperature': esp_data.get('temperature'),
                        'humidity': esp_data.get('humidity'),
                        'pressure': esp_data.get('pressure'),
                        'status': 'online'
                    })
                else:
                    sensor_data['status'] = 'offline'
                    print(f"Error: Received status code {response.status_code} from ESP32")
            except requests.RequestException as e:
                sensor_data['status'] = 'offline'
                print(f"Error fetching data from ESP32: {e}")

    return jsonify(sensor_data)


@app.route('/check_device_status', methods=['POST'])
def check_device_status():
    data = request.get_json()
    device_ip = data.get('device_ip')
    device_type = data.get('device_type')

    if not device_ip or not device_type:
        return jsonify({'error': 'Missing device_ip or device_type'}), 400

    if device_type == 'fronius':
        # ➔ Special check for fronius
        online = check_fronius_device(device_ip)
    else:
        # ➔ For all others, call their /status or /state API
        online = check_normal_device(device_ip)

    return jsonify({'online': online})


def check_fronius_device(device_ip):
    # Custom logic for Fronius devices
    try:
        # Example: call their Solar API
        url = f"http://{device_ip}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking Fronius device: {e}")
        return False


def check_normal_device(device_ip):
    # For regular smart plugs, thermostats, etc.
    try:
        if ':' in device_ip:
            ip, port = device_ip.split(':')
        else:
            ip = device_ip
            port = 80  # default

        # Example: assume all devices expose a /status endpoint
        url = f"http://{ip}:{port}/sensor-data"
        response = requests.get(url, timeout=2)

        if response.status_code == 200:
            status_info = response.json()
            # Expecting JSON: {"state": "on"} or {"state": "off"}
            return status_info.get('state') == 'on'
        else:
            return False
    except Exception as e:
        print(f"Error checking normal device: {e}")
        return False


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
