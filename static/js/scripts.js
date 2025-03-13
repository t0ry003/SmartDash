function toggleOn(deviceName, deviceIp) {
    var bulbIcon = document.getElementById('bulb-icon-' + deviceName);
    var state = 'off';

    if (bulbIcon.style.color === 'yellow') {
        bulbIcon.style.color = 'gray';
        bulbIcon.style.textShadow = 'none';
    } else {
        bulbIcon.style.color = 'yellow';
        bulbIcon.style.textShadow = '0 0 10px yellow';

        state = 'on';
    }

    fetch('/toggle_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            device_name: deviceName,
            device_ip: deviceIp,
            state: state,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => console.error('Error:', error));
}

function showMenu(menuName, isHome, isSettings = false, isSolar = false, isTemp = false) {
    document.getElementById('main-content').classList.toggle('d-none', !isHome);
    document.getElementById('solar-panel-data').classList.toggle('d-none', !isSolar);
    document.getElementById('temperature-data').classList.toggle('d-none', !isTemp);
    document.getElementById('appearance-menu').classList.toggle('d-none', !isSettings);
    document.getElementById('account-menu').classList.toggle('d-none', !isSettings);
    document.getElementById('about-menu').classList.toggle('d-none', !isSettings);
}

function changeTheme(theme) {
    if (theme === 'light') {
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
    } else {
        document.body.style.backgroundColor = '#121212';
        document.body.style.color = 'white';
    }
}

function fetchSolarData() {
    fetch('/solar-data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('solar-power').textContent = `${data.power}`;
            document.getElementById('solar-energy').textContent = `${data.energy_produced}`;
            document.getElementById('solar-energy-consumed').textContent = `${data.energy_consumed}`;
            document.getElementById('solar-net-balance').textContent = `${data.net_energy_balance}`;
            document.getElementById('solar-self-sufficiency').textContent = `${data.self_sufficiency}`;

            document.getElementById('solar-grid-import').textContent = `${data.grid_import}`;
            document.getElementById('solar-grid-export').textContent = `${data.grid_export}`;

            document.getElementById('solar-voltage-1').textContent = `${data.voltage_phase_1}`;
            document.getElementById('solar-voltage-2').textContent = `${data.voltage_phase_2}`;
            document.getElementById('solar-voltage-3').textContent = `${data.voltage_phase_3}`;

            document.getElementById('solar-current-1').textContent = `${data.current_phase_1}`;
            document.getElementById('solar-current-2').textContent = `${data.current_phase_2}`;
            document.getElementById('solar-current-3').textContent = `${data.current_phase_3}`;

            document.getElementById('solar-power-factor').textContent = data.power_factor;
            document.getElementById('solar-reactive-power').textContent = `${data.reactive_power}`;

            document.getElementById('solar-co2').textContent = `${data.co2_savings}`;
        })
        .catch(error => {
            console.error('Error fetching solar data:', error);
            const errorMessage = 'Error fetching data';
            document.getElementById('solar-power').textContent = errorMessage;
            document.getElementById('solar-energy').textContent = errorMessage;
            document.getElementById('solar-voltage-1').textContent = errorMessage;
        });
}

setInterval(fetchSolarData, 20000);
fetchSolarData();

function fetchTemperatureData() {
    fetch('/temperature-data')
        .then(response => response.json())
        .then(data => {
            const temperatureElement = document.getElementById('temperature');
            const humidityElement = document.getElementById('humidity');
            const thermometerFill = document.getElementById('thermometer-fill');
            const temperatureIcon = document.querySelector("#temperature-icon");


            const temperature = data.temperature;
            const humidity = data.humidity;

            temperatureElement.textContent = `Temperature: ${temperature}°C`;
            humidityElement.textContent = `Humidity: ${humidity}%`;

            let iconClass = "fa-thermometer-empty";
            if (temperature > 10) iconClass = "fa-thermometer-quarter";
            if (temperature > 20) iconClass = "fa-thermometer-half";
            if (temperature > 30) iconClass = "fa-thermometer-three-quarters";
            if (temperature > 40) iconClass = "fa-thermometer-full";

             temperatureIcon.className = `fa-solid ${iconClass}`;

            // Calculate the fill height based on temperature
            const minTemp = 0; // Minimum temperature expected
            const maxTemp = 50; // Maximum temperature expected


            // Set the fill height and color
            // thermometerFill.style.height = `${fillHeight}%`;

            temperatureIcon.style.color = getTemperatureColor(temperature)
        })
        .catch(error => {
            console.error('Error fetching temperature data:', error);
            document.getElementById('temperature').textContent = `Error fetching data: ${error}`;
            document.getElementById('humidity').textContent = `Error fetching data: ${error}`;
        });
}

function getTemperatureColor(temperature) {
    // Define color thresholds
    if (temperature <= 5) {
        return '#264653';
    } else if (temperature <= 10) {
        return '#2a9d8f';
    } else if (temperature <= 20) {
        return '#e9c46a';
    }  else if (temperature <= 25) {
        return '#f4a261';
    }else {
        return '#e76f51';
    }
}

setInterval(fetchTemperatureData, 1000);
fetchTemperatureData();


document.addEventListener("DOMContentLoaded", function () {
    // Load user settings from backend when the page loads
    fetch('/get_settings')
        .then(response => response.json())
        .then(data => {
            if (data.theme) {
                document.getElementById("theme-select").value = data.theme;
                changeTheme(data.theme);
            }
            if (data.show_ip !== undefined) {
                document.getElementById("show-ip-checkbox").checked = data.show_ip;
                toggleIPVisibility(document.getElementById("show-ip-checkbox"));
            }
        });

    // Function to save settings
    function saveSettings() {
        const settings = {
            theme: document.getElementById("theme-select").value,
            show_ip: document.getElementById("show-ip-checkbox").checked
        };

        fetch('/save_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        }).then(response => response.json())
            .then(data => console.log(data.message));
    }

    // Function to toggle IP visibility
    function toggleIPVisibility(checkbox) {
        var ipElements = document.querySelectorAll('.device-ip');

        ipElements.forEach(function (ipElement) {
            if (checkbox.checked) {
                ipElement.style.display = 'block';
            } else {
                ipElement.style.display = 'none';
            }
        });
    }

    let pressTimer;

    window.showContextMenu = function (event, deviceName) {
        event.preventDefault(); // Prevent default right-click or long-press behavior

        // Close any open context menus
        document.querySelectorAll(".context-menu").forEach(menu => {
            menu.style.display = "none";
        });

        // Get the correct menu
        let contextMenu = document.getElementById(`context-menu-${deviceName}`);
        if (contextMenu) {
            contextMenu.style.top = `${event.pageY}px`;
            contextMenu.style.left = `${event.pageX}px`;
            contextMenu.style.display = "block";
        }
    };

    // Hide context menu when clicking outside
    document.addEventListener("click", function () {
        document.querySelectorAll(".context-menu").forEach(menu => {
            menu.style.display = "none";
        });
    });

    // Handle long press for mobile
    document.querySelectorAll(".device-card").forEach(element => {
        let deviceName = element.getAttribute("data-device-name");

        // Touch start (begin holding)
        element.addEventListener("touchstart", function (event) {
            pressTimer = setTimeout(() => showContextMenu(event, deviceName), 600); // Trigger after 600ms
        });

        // Cancel long-press if user lifts finger
        element.addEventListener("touchend", function () {
            clearTimeout(pressTimer);
        });

        // Cancel long-press if user moves finger
        element.addEventListener("touchmove", function () {
            clearTimeout(pressTimer);
        });
    });

    // Event listeners for changes
    document.getElementById("theme-select").addEventListener("change", saveSettings);
    document.getElementById("show-ip-checkbox").addEventListener("change", function (e) {
        toggleIPVisibility(e.target);
        saveSettings();
    });


});