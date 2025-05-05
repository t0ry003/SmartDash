import os
import re

import markdown
from flask import Blueprint, render_template, url_for, request
from markupsafe import Markup

device_setup_bp = Blueprint('device_setup', __name__, template_folder='templates', static_folder='static')

qualified_devices = {"ESP32_THERMOSTAT_DHT11_BMP180"}


@device_setup_bp.route('/')
def index():
    project_root = os.path.join('device_setup', 'projects')

    projects = []
    for project in os.listdir(project_root):
        image_file = os.path.join(project_root, project, 'breadboard.png')
        # Try to check if breadboard image actually exists
        if os.path.exists(image_file):
            image_url = url_for('device_setup.static', filename=f'projects/{project}/breadboard.png')
        else:
            image_url = url_for('device_setup.static', filename='default.png')

        projects.append({
            'name': project,
            'image_url': image_url,
            'qualified': project in qualified_devices
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

        if request.method == 'POST':
            ssid = request.form.get('ssid', '')
            password = request.form.get('password', '')
            # Replace placeholders in the code
            code = re.sub(r'const char\* ssid = ".*?";', f'const char* ssid = "{ssid}";', code)
            code = re.sub(r'const char\* password = ".*?";', f'const char* password = "{password}";', code)

        return render_template('device_setup/project.html',
                               project_name=project_name,
                               code=code,
                               guide=guide_html,
                               generic_guide=generic_html,
                               image_url=image_url,
                               qualification=project_name in qualified_devices,
                               ssid=ssid,
                               password=password)

    except FileNotFoundError:
        return f"Project '{project_name}' not found", 404
