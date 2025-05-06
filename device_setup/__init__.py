import os
import re

import markdown
from flask import Blueprint, render_template, url_for, request
from markupsafe import Markup

device_setup_bp = Blueprint('device_setup', __name__, template_folder='templates', static_folder='static')

qualified_devices = {"ESP32_THERMOSTAT_DHT11_BMP180", "ESP32_RELAY"}
thermostat_devices = {"ESP32_THERMOSTAT_DHT11_BMP180", "ESP32_THERMOSTAT_DHT11", "ESP32_THERMOSTAT_BMP180"}
relay_devices = {"ESP32_RELAY"}


@device_setup_bp.route('/')
def index():
    project_root = os.path.join('device_setup', 'projects')

    projects = []
    for proj in os.listdir(project_root):
        image_file = os.path.join(project_root, proj, 'breadboard.png')
        # Try to check if breadboard image actually exists
        if os.path.exists(image_file):
            image_url = url_for('device_setup.static', filename=f'projects/{proj}/breadboard.png')
        else:
            image_url = url_for('device_setup.static', filename='default.png')

        projects.append({
            'name': proj,
            'image_url': image_url,
            'qualified': proj in qualified_devices
        })

    return render_template('device_setup/index.html', projects=projects)


@device_setup_bp.route('/<project_name>', methods=['GET', 'POST'])
def project(project_name):
    project_root = os.path.join('device_setup')
    base_path = os.path.join('device_setup', 'projects', project_name)
    try:
        with open(os.path.join(base_path, 'code.ino'), encoding='utf-8') as f:
            code = f.read()

        with open(os.path.join(base_path, 'guide.md'), encoding='utf-8') as f:
            guide_md = f.read()
            guide_html = Markup(markdown.markdown(guide_md, extensions=[
                "extra",  # includes tables, fenced_code, etc.
                "codehilite",  # syntax highlighting
                "toc",  # table of contents
                "nl2br",  # line breaks to <br>
                "smarty",  # smart quotes
            ]))

        with open(os.path.join(project_root, 'generic_guide.md'), encoding='utf-8') as f:
            generic_md = f.read()
            generic_html = Markup(markdown.markdown(generic_md, extensions=[
                "extra",
                "codehilite",
                "toc",
                "nl2br",
                "smarty",
            ]))

        image_url = url_for('device_setup.static', filename=f'projects/{project_name}/breadboard.png')

        ssid = ''
        password = ''
        gpio = '5'

        if request.method == 'POST':
            ssid = request.form.get('ssid', '')
            password = request.form.get('password', '')
            gpio = request.form.get('gpio', '')
            # Replace placeholders in the code
            code = re.sub(r'const char\* ssid = ".*?";', f'const char* ssid = "{ssid}";', code)
            code = re.sub(r'const char\* password = ".*?";', f'const char* password = "{password}";', code)
            if not gpio:
                gpio = '5'

            if project_name in thermostat_devices:
                code = re.sub(r'#define DHTPIN \d+', f'#define DHTPIN {gpio}', code)
            elif project_name in relay_devices:
                code = re.sub(r'#define RELAY_PIN \d+', f'#define RELAY_PIN {gpio}', code)
            else:
                code = re.sub(r'#define GPIO_PIN \d+', f'#define GPIO_PIN {gpio}', code)

        return render_template('device_setup/project.html',
                               project_name=project_name,
                               code=code,
                               guide=guide_html,
                               generic_guide=generic_html,
                               image_url=image_url,
                               qualification=project_name in qualified_devices,
                               ssid=ssid,
                               password=password,
                               gpio=gpio
                               )

    except FileNotFoundError:
        return f"Project '{project_name}' not found", 404
