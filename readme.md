<div align="center">
  <img src="static/images/0.5x/Artboard%201@0.5x.png" alt="SmartDash" width="400">
</div>

<h1 align="center">SmartDash</h1>

<div align="center">
  <h3 align="center">📡 A modern web application to monitor and manage your smart devices effortlessly from a centralized dashboard.</h3>
  <p align="center">
    <a href="#-installation">Installation</a> •
    <a href="#️-database-integration">Database Integration</a> •
    <a href="#-hardware-setup">Hardware</a> •
    <a href="https://github.com/t0ry003/SmartDash/wiki">Wiki</a>
  </p>

[![GitHub Stars](https://img.shields.io/github/stars/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/pulls)
[![License](https://img.shields.io/github/license/t0ry003/SmartDash.svg)](https://github.com/t0ry003/SmartDash/blob/main/LICENSE)
</div>

---

## 📋 Overview

**SmartDash** is a lightweight, flexible, and easy-to-use web dashboard designed to manage and monitor your smart home
devices.  
Built with **Python (Flask)** and **JavaScript**, it enables you to connect to various databases and offers a
streamlined setup experience.

Key Features:

- 📱 Centralized control panel for your smart devices
- ⚡ Quick and easy database configuration
- 🧩 Modular architecture for future expansion
- 🌐 Built using Flask and modern frontend technologies

To be added:

- ESP32 website flasher;
- Hardware diagrams for ESP32 (SmartPlug, SmartSwitch, SmartLight, Thermostat, etc.);
- Larger solar inverters brand support;

---

## 🚀 Installation

### Target of this project

The target of this project is to create your own smart home dashboard on your old computer or Raspberry Pi. It is
designed to be lightweight and easy to set up, making it perfect for those who want to create a smart home system
without the need for expensive hardware or complex software. Since Home Assistant is a bit heavy for Raspberry Pi, this
project is designed to be lightweight and easy to set up for those who want to learn about smart home systems and create
their own dashboard. This project is not intended to be a full-fledged smart home system, but rather a starting point
for those who want to learn about smart home systems and create their own dashboard. It is designed to be modular and
extensible, allowing you to add your own features and functionality as needed.

### Prerequisites

- Python **3.10** or **3.11**
- `pip` (Python package manager)
- A supported database (**PostgreSQL**, **MSSQL**, **MySQL**, **MariaDB**, Firebird, Sybase)

### Setup Instructions

1. **Clone the repository:**
    ```bash
    git clone https://github.com/t0ry003/SmartDash.git
    cd SmartDash
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Activate the virtual environment
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run initial setup and database configuration:**
    ```bash
    python app.py
    ```
   This will guide you through generating a `config.json` file based on your database credentials.

---

## ⚙️ Database Integration

### Tested Databases

- **PostgreSQL**: PostgreSQL (https://www.postgresql.org/)
- **MSSQL**: Microsoft SQL Server (https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- **MySQL**: MySQL (https://www.mysql.com/)
- **MariaDB**: MariaDB (https://mariadb.org/)

### Database Setup

**PostgreSQL (Recommended)** - https://www.w3schools.com/postgresql/postgresql_install.php

#### Why we recommend PostgreSQL?

- **[neon.tech](https://neon.tech/)**: Neon is a serverless PostgreSQL database that allows you to create a free
  database with a single click. It is easy to set up and provides a great user experience.
- **DIY**: If you prefer to set up your own PostgreSQL database, you can do so by following the instructions on the
  official PostgreSQL website. It provides detailed documentation on how to install and configure PostgreSQL on various
  platforms.
- **Performance**: PostgreSQL is known for its high performance and scalability, making it suitable for handling large
  datasets and complex queries.

---

## 🛠️ Hardware Setup

### ESP32

#### SmartPlug, SmartLight

<!-- ESP32 Relay -->
<div align="center">
  <img src="/dev/relay.png" alt="ESP32 Relay" style="max-width: 80%; height: auto;" />
  <p>ESP32 Relay</p>
  <a href="https://github.com/t0ry003/SmartDash/blob/master/dev/esp32_relay.ino" >
    <img src="https://img.shields.io/badge/ESP32_Relay_Code-View-blue?logo=github" alt="ESP32 Relay Code" />
  </a>
</div>

#### Thermostat

<!-- ESP32 Thermostat DHT11 + BMP180 -->
<div align="center">
  <img src="/dev/dht_bmp.png" alt="ESP32 Thermostat DHT11 + BMP180" style="max-width: 80%; height: auto;" />
  <p>ESP32 Thermostat DHT11 + BMP180</p>
  <a href="https://github.com/t0ry003/SmartDash/blob/master/dev/esp32_thermostat_DHT11_BMP180.ino">
    <img src="https://img.shields.io/badge/ESP32_Thermostat_DHT11_+_BMP180_Code-View-blue?logo=github" alt="ESP32 Thermostat DHT11 + BMP180 Code" />
  </a>
</div>

<br>

<!-- ESP32 Thermostat DHT11 -->
<div align="center">
  <img src="/dev/dht.png" alt="ESP32 Thermostat DHT11" style="max-width: 80%; height: auto;" />
  <p>ESP32 Thermostat DHT11</p>
  <a href="https://github.com/t0ry003/SmartDash/blob/master/dev/esp32_thermostat_DHT11.ino">
    <img src="https://img.shields.io/badge/ESP32_Thermostat_DHT11_Code-View-blue?logo=github" alt="ESP32 Thermostat DHT11 Code" />
  </a>
</div>

<br>

<!-- ESP32 Thermostat BMP180 -->
<div align="center">
  <img src="/dev/bmp.png" alt="ESP32 Thermostat BMP180" style="max-width: 80%; height: auto;" />
  <p>ESP32 Thermostat BMP180</p>
  <a href="https://github.com/t0ry003/SmartDash/blob/master/dev/esp32_thermostat_BMP180.ino">
    <img src="https://img.shields.io/badge/ESP32_Thermostat_BMP180-View-blue?logo=github" alt="ESP32 Thermostat BMP180 Code" />
  </a>
</div>