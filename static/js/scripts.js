function hexToRgb(hex) {
    hex = hex.replace(/^#/, ""); // Remove "#" if present

    let r = parseInt(hex.substring(0, 2), 16);
    let g = parseInt(hex.substring(2, 4), 16);
    let b = parseInt(hex.substring(4, 6), 16);

    return `rgb(${r}, ${g}, ${b})`; // Remove alpha because getComputedStyle() does not use it
}


function toggleOn(deviceName, deviceIp, deviceType) {
    var bulbIcon = document.getElementById('bulb-icon-' + deviceName);
    var state = 'off';

    const newColor = hexToRgb("#52887A3F");
    const color = window.getComputedStyle(bulbIcon).color;

    // Show menu based on device type without toggling icon
    if (deviceType === 'fronius') {
        showMenu('solar');
        return;
    } else if (deviceType === 'thermostat') {
        showMenu('temp');
        return;
    } else if (deviceType === 'sensor') {
        return; // Do nothing
    }

    // Toggle icon color for other device types
    if (color === newColor) {
        bulbIcon.style.color = 'gray';
        bulbIcon.style.textShadow = 'none';
        bulbIcon.style.transition = 'color 0.3s ease-in-out, text-shadow 0.3s ease-in-out';
    } else {
        bulbIcon.style.color = newColor;
        bulbIcon.style.textShadow = `0 0 10px ${newColor}`;
        bulbIcon.style.transition = 'color 0.3s ease-in-out, text-shadow 0.3s ease-in-out';
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
            device_type: deviceType,
            state: state,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => console.error('Error:', error));
}

function showMenu(menuName) {
    const menuMap = {
        home: ['main-content'],
        solar: ['solar-panel-data'],
        temp: ['temperature-data'],
        settings: ['appearance-menu', 'account-menu', 'about-menu']
    };

    // Hide all menus first
    Object.values(menuMap).flat().forEach(id => {
        document.getElementById(id).classList.add('d-none');
    });

    // Show selected menu
    if (menuMap[menuName]) {
        menuMap[menuName].forEach(id => {
            document.getElementById(id).classList.remove('d-none');
        });
    }
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
            const humidityIcon = document.querySelector("#humidity-icon");
            const pressureIcon = document.querySelector("#pressure-icon");
            const pressureElement = document.getElementById('pressure');
            const pressureFill = document.getElementById('pressure-fill');

            const temperature = data.temperature;
            const humidity = data.humidity;
            const pressure = data.pressure;

            temperatureElement.textContent = `Temperature: ${temperature}°C`;
            humidityElement.textContent = `Humidity: ${humidity}%`;
            pressureElement.textContent = `Pressure: ${pressure} hPa`;
            let iconClass = "fa-thermometer-empty";
            if (temperature > 10) iconClass = "fa-thermometer-quarter";
            if (temperature > 20) iconClass = "fa-thermometer-half";
            if (temperature > 30) iconClass = "fa-thermometer-three-quarters";
            if (temperature > 40) iconClass = "fa-thermometer-full";


            humidityIcon.style.color = getHumidityColor(humidity);
            pressureIcon.style.color = getPressureColor(pressure);

            temperatureIcon.className = `fa-solid ${iconClass}`;

            // Calculate the fill height based on temperature
            const minTemp = 0; // Minimum temperature expected
            const maxTemp = 50; // Maximum temperature expected


            temperatureIcon.style.color = getTemperatureColor(temperature)


        })
        .catch(error => {
            console.error('Error fetching temperature data:', error);
            document.getElementById('temperature').textContent = `Error fetching data: ${error}`;
            document.getElementById('humidity').textContent = `Error fetching data: ${error}`;
            document.getElementById('pressure').textContent = 'Error fetching data';
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
    } else if (temperature <= 25) {
        return '#f4a261';
    } else {
        return '#e76f51';
    }
}

function getHumidityColor(humidity) {
    if (humidity < 30) return "#caf0f8"; // Dry air
    else if (humidity < 50) return "#00b4d8";
    else if (humidity < 70) return "#0077b6";
    else return "#023e8a"// Normal air

}

function getPressureColor(pressure) {
    if (pressure >= 1020) return "#28a745"; // High pressure
    else if (pressure >= 1000) return "#f1c40f";  // Normal pressure
    else if (pressure >= 980) return "#e67e22";  //  Low pressure
    else return "#e74c3c"; // Very low pressure
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
    // Graphics
    let powerEnergyChart, gridImportExportChart, voltagePhaseChart, currentMetricsChart;

    function updateCharts(data) {
        // Power & Energy Chart Data
        const powerEnergyData = [data.energy_produced, data.energy_consumed, data.net_energy_balance];
        const powerEnergyLabels = ["Energy Produced (kWh)", "Energy Consumed (kWh)", "Net Balance (kWh)"];
        const powerEnergyColors = ["#28a745", "#f39c12", "#8e44ad"];

        if (!powerEnergyChart) {
            const ctx = document.getElementById("powerEnergyChart").getContext("2d");
            powerEnergyChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: powerEnergyLabels,
                    datasets: [{
                        label: "Power & Energy",
                        data: powerEnergyData,
                        backgroundColor: powerEnergyColors
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "kWh"
                            }
                        },
                        y: {
                            suggestedMin: 0,
                            suggestedMax: Math.max(...powerEnergyData) + 100,
                            title: {display: true}
                        }
                    },
                    plugins: {
                        legend: {display: false}
                    }
                }
            });
        } else {
            powerEnergyChart.data.datasets[0].data = powerEnergyData;
            powerEnergyChart.update();
        }
        // Grid Import/Export Chart
        const gridData = [data.grid_import, data.grid_export];
        const gridLabels = ["Grid Import (kWh)", "Grid Export (kWh)"];

        if (!gridImportExportChart) {
            const ctx2 = document.getElementById("gridImportExportChart").getContext("2d");
            gridImportExportChart = new Chart(ctx2, {
                type: "bar",
                data: {
                    labels: gridLabels,
                    datasets: [{
                        label: "Grid Import/Export",
                        data: gridData,
                        backgroundColor: ["#ff5733", "#f2079c"]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "kWh"
                            }
                        },
                        y: {
                            title: {display: true}
                        }
                    },
                    plugins: {
                        legend: {display: false}
                    }
                }
            });
        } else {
            gridImportExportChart.data.datasets[0].data = gridData;
            gridImportExportChart.update();
        }

        const voltageData = [data.voltage_phase_1, data.voltage_phase_2, data.voltage_phase_3];
        const voltageLabels = ["Phase 1 (V)", "Phase 2 (V)", "Phase 3 (V)"];

        if (!voltagePhaseChart) {
            const ctx3 = document.getElementById("voltagePhaseChart").getContext("2d");
            voltagePhaseChart = new Chart(ctx3, {
                type: "line",
                data: {
                    labels: voltageLabels,
                    datasets: [{
                        label: "Voltage Phase",
                        data: voltageData,
                        borderColor: "#ff9900",
                        backgroundColor: "rgba(255, 153, 0, 0.2)",
                        borderWidth: 3,
                        pointRadius: 5,
                        pointBackgroundColor: "#ff6600",
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            grid: {
                                borderDash: [5, 5]
                            }
                        }
                    }
                }
            });
        } else {
            voltagePhaseChart.data.datasets[0].data = voltageData;
            voltagePhaseChart.update();
        }
        // Current & Other Metrics Chart Data
        const currentMetricsData = [data.current_phase_1, data.current_phase_2, data.current_phase_3];
        const currentMetricsLabels = ["Current Phase 1 (A)", "Current Phase 2 (A)", "Current Phase 3 (A)"];

        if (!currentMetricsChart) {
            const ctx3 = document.getElementById("currentMetricsChart").getContext("2d");
            currentMetricsChart = new Chart(ctx3, {
                type: "doughnut",
                data: {
                    labels: currentMetricsLabels,
                    datasets: [{
                        label: "Current & Other Metrics",
                        data: currentMetricsData,
                        backgroundColor: ["#1abc9c", "#3498db", "#f1c40f"],
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'right',
                            labels: {
                                boxWidth: 20,
                                padding: 10
                            }
                        }
                    }
                }
            });
        } else {
            currentMetricsChart.data.datasets[0].data = currentMetricsData;
            currentMetricsChart.update();
        }
    }

    function fetchSolarData() {
        fetch("/solar-data")
            .then(response => response.json())
            .then(data => updateCharts(data))
            .catch(error => console.error("Error fetching solar data:", error));
    }

    setInterval(fetchSolarData, 5000);


});