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

function showMenu(menuName, isHome, isSettings = false) {
    document.getElementById('main-content').classList.toggle('d-none', !isHome);
    document.getElementById('menu-screen').classList.toggle('d-none', isHome || isSettings);
    document.getElementById('appearance-menu').classList.toggle('d-none', !isSettings);
    document.getElementById('account-menu').classList.toggle('d-none', !isSettings);
    document.getElementById('about-menu').classList.toggle('d-none', !isSettings);


    if (!isHome && !isSettings) {
        document.getElementById('menu-message').innerText = menuName + ' Screen';
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