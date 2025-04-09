function hexToRgb(e) {
    let t = parseInt((e = e.replace(/^#/, "")).substring(0, 2), 16), n;
    return `rgb(${t}, ${parseInt(e.substring(2, 4), 16)}, ${parseInt(e.substring(4, 6), 16)})`
}

function toggleOn(e, t, n) {
    var o = document.getElementById("bulb-icon-" + e), a = "off";
    let r = hexToRgb("#52887A3F"), l = window.getComputedStyle(o).color;
    if ("fronius" === n) {
        showMenu("solar");
        return
    }
    if ("thermostat" === n) {
        showMenu("temp");
        return
    }
    "sensor" !== n && (l === r ? (o.style.color = "gray", o.style.textShadow = "none", o.style.transition = "color 0.3s ease-in-out, text-shadow 0.3s ease-in-out") : (o.style.color = r, o.style.textShadow = `0 0 10px ${r}`, o.style.transition = "color 0.3s ease-in-out, text-shadow 0.3s ease-in-out", a = "on"), fetch("/toggle_device", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({device_name: e, device_ip: t, device_type: n, state: a})
    }).then(e => e.json()).then(e => {
        console.log(e.message)
    }).catch(e => console.error("Error:", e)))
}

function showMenu(e) {
    let t = {
        home: ["main-content"],
        solar: ["solar-panel-data"],
        temp: ["temperature-data"],
        settings: ["appearance-menu", "account-menu", "help-menu", "about-menu"]
    };
    Object.values(t).flat().forEach(e => {
        document.getElementById(e).classList.add("d-none")
    }), t[e] && t[e].forEach(e => {
        document.getElementById(e).classList.remove("d-none")
    })
}

function autoUploadProfilePicture(e) {
    if (e.files && e.files[0]) {
        let t = e.files[0];
        if (!["image/png", "image/jpeg"].includes(t.type)) {
            alert("Only PNG and JPG files are allowed.");
            return
        }
        if (t.size > 2097152) {
            alert("File size must be less than 2MB.");
            return
        }
        let n = new FormData;
        n.append("profile_picture", t);
        let o = document.createElement("div");
        o.className = "loading-spinner";
        let a = e.closest(".profile-picture-wrapper");
        a.appendChild(o), fetch("/upload_profile_picture", {method: "POST", body: n}).then(e => {
            e.ok ? location.reload() : e.text().then(e => {
                alert(`Failed to upload profile picture: ${e}`)
            })
        }).catch(e => {
            console.error("Error:", e), alert("An error occurred while uploading the profile picture.")
        }).finally(() => {
            o.remove()
        })
    }
}

function showChangePasswordModal() {
    new bootstrap.Modal(document.getElementById("changePasswordModal")).show()
}

function changeTheme(e) {
    console.log("Theme selected:", e), "light" === e ? (document.body.classList.add("light-theme"), document.body.style.setProperty("background-color", "white", "important"), document.body.style.setProperty("color", "white", "important")) : (document.body.classList.add("dark-theme"), document.body.style.backgroundColor = "#212529", document.body.style.color = "white"), localStorage.setItem("theme", e)
}

function fetchSolarData() {
    fetch("/solar-data").then(e => e.json()).then(e => {
        document.getElementById("solar-power").textContent = `${e.power}`, document.getElementById("solar-energy").textContent = `${e.energy_produced}`, document.getElementById("solar-energy-consumed").textContent = `${e.energy_consumed}`, document.getElementById("solar-net-balance").textContent = `${e.net_energy_balance}`, document.getElementById("solar-self-sufficiency").textContent = `${e.self_sufficiency}`, document.getElementById("solar-grid-import").textContent = `${e.grid_import}`, document.getElementById("solar-grid-export").textContent = `${e.grid_export}`, document.getElementById("solar-voltage-1").textContent = `${e.voltage_phase_1}`, document.getElementById("solar-voltage-2").textContent = `${e.voltage_phase_2}`, document.getElementById("solar-voltage-3").textContent = `${e.voltage_phase_3}`, document.getElementById("solar-current-1").textContent = `${e.current_phase_1}`, document.getElementById("solar-current-2").textContent = `${e.current_phase_2}`, document.getElementById("solar-current-3").textContent = `${e.current_phase_3}`, document.getElementById("solar-power-factor").textContent = e.power_factor, document.getElementById("solar-reactive-power").textContent = `${e.reactive_power}`, document.getElementById("solar-co2").textContent = `${e.co2_savings}`
    }).catch(e => {
        console.error("Error fetching solar data:", e);
        let t = "Error fetching data";
        document.getElementById("solar-power").textContent = t, document.getElementById("solar-energy").textContent = t, document.getElementById("solar-voltage-1").textContent = t
    })
}

function fetchTemperatureData() {
    fetch("/temperature-data").then(e => e.json()).then(e => {
        let t = document.getElementById("temperature"), n = document.getElementById("humidity");
        document.getElementById("thermometer-fill");
        let o = document.querySelector("#temperature-icon"), a = document.querySelector("#humidity-icon"),
            r = document.querySelector("#pressure-icon"), l = document.getElementById("pressure");
        document.getElementById("pressure-fill");
        let s = e.temperature, d = e.humidity, i = e.pressure;
        t.textContent = `Temperature: ${s}\xb0C`, n.textContent = `Humidity: ${d}%`, l.textContent = `Pressure: ${i} hPa`;
        let c = "fa-thermometer-empty";
        s > 10 && (c = "fa-thermometer-quarter"), s > 20 && (c = "fa-thermometer-half"), s > 30 && (c = "fa-thermometer-three-quarters"), s > 40 && (c = "fa-thermometer-full"), a.style.color = getHumidityColor(d), r.style.color = getPressureColor(i), o.className = `fa-solid ${c}`, o.style.color = getTemperatureColor(s)
    }).catch(e => {
        console.error("Error fetching temperature data:", e), document.getElementById("temperature").textContent = `Error fetching data: ${e}`, document.getElementById("humidity").textContent = `Error fetching data: ${e}`, document.getElementById("pressure").textContent = `Error fetching data: ${e}`
    })
}

function getTemperatureColor(e) {
    return e <= 5 ? "#264653" : e <= 10 ? "#2a9d8f" : e <= 20 ? "#e9c46a" : e <= 25 ? "#f4a261" : "#e76f51"
}

function getHumidityColor(e) {
    return e < 30 ? "#caf0f8" : e < 50 ? "#00b4d8" : e < 70 ? "#0077b6" : "#023e8a"
}

function getPressureColor(e) {
    return e <= 980 ? "#28a745" : e <= 1e3 ? "#f1c40f" : e <= 1200 ? "#e67e22" : "#e74c3c"
}

document.addEventListener("DOMContentLoaded", function () {
    document.body.style.overflow = "auto"
}), document.addEventListener("DOMContentLoaded", function () {
    let e = document.querySelectorAll(".alert");
    e.forEach(e => {
        setTimeout(() => {
            e.classList.add("fade-out")
        }, 5e3)
    })
}), window.onload = function () {
    let e = localStorage.getItem("theme"), t = document.getElementById("theme-select");
    e && (changeTheme(e), t.value = e)
}, setInterval(fetchSolarData, 2e4), fetchSolarData(), setInterval(fetchTemperatureData, 1e3), fetchTemperatureData(), document.addEventListener("DOMContentLoaded", function () {
    function e() {
        let e = {
            theme: document.getElementById("theme-select").value,
            show_ip: document.getElementById("show-ip-checkbox").checked
        };
        fetch("/save_settings", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(e)
        }).then(e => e.json()).then(e => console.log(e.message))
    }

    function t(e) {
        document.querySelectorAll(".device-ip").forEach(function (t) {
            e.checked ? t.style.display = "block" : t.style.display = "none"
        })
    }

    fetch("/get_settings").then(e => e.json()).then(e => {
        e.theme && (document.getElementById("theme-select").value = e.theme, changeTheme(e.theme)), void 0 !== e.show_ip && (document.getElementById("show-ip-checkbox").checked = e.show_ip, t(document.getElementById("show-ip-checkbox")))
    });
    let n;
    window.showContextMenu = function (e, t) {
        e.preventDefault(), document.querySelectorAll(".context-menu").forEach(e => {
            e.style.display = "none"
        });
        let n = document.getElementById(`context-menu-${t}`);
        n && (n.style.top = `${e.pageY}px`, n.style.left = `${e.pageX}px`, n.style.display = "block")
    }, document.addEventListener("click", function () {
        document.querySelectorAll(".context-menu").forEach(e => {
            e.style.display = "none"
        })
    }), document.querySelectorAll(".device-card").forEach(e => {
        let t = e.getAttribute("data-device-name");
        e.addEventListener("touchstart", function (e) {
            n = setTimeout(() => showContextMenu(e, t), 600)
        }), e.addEventListener("touchend", function () {
            clearTimeout(n)
        }), e.addEventListener("touchmove", function () {
            clearTimeout(n)
        })
    }), document.getElementById("theme-select").addEventListener("change", e), document.getElementById("show-ip-checkbox").addEventListener("change", function (n) {
        t(n.target), e()
    });
    let o, a, r, l;
    setInterval(function e() {
        fetch("/solar-data").then(e => e.json()).then(e => (function e(t) {
            let n = [t.energy_produced, t.energy_consumed, t.net_energy_balance];
            if (o) o.data.datasets[0].data = n, o.update(); else {
                let s = document.getElementById("powerEnergyChart").getContext("2d");
                o = new Chart(s, {
                    type: "bar",
                    data: {
                        labels: ["Energy Produced (kWh)", "Energy Consumed (kWh)", "Net Balance (kWh)"],
                        datasets: [{
                            label: "Power & Energy",
                            data: n,
                            backgroundColor: ["#28a745", "#f39c12", "#8e44ad"]
                        }]
                    },
                    options: {
                        responsive: !0,
                        maintainAspectRatio: !1,
                        scales: {
                            x: {title: {display: !0, text: "kWh"}},
                            y: {suggestedMin: 0, suggestedMax: Math.max(...n) + 100, title: {display: !0}}
                        },
                        plugins: {legend: {display: !1}}
                    }
                })
            }
            let d = [t.grid_import, t.grid_export];
            if (a) a.data.datasets[0].data = d, a.update(); else {
                let i = document.getElementById("gridImportExportChart").getContext("2d");
                a = new Chart(i, {
                    type: "bar",
                    data: {
                        labels: ["Grid Import (kWh)", "Grid Export (kWh)"],
                        datasets: [{label: "Grid Import/Export", data: d, backgroundColor: ["#ff5733", "#f2079c"]}]
                    },
                    options: {
                        responsive: !0,
                        maintainAspectRatio: !1,
                        scales: {x: {title: {display: !0, text: "kWh"}}, y: {title: {display: !0}}},
                        plugins: {legend: {display: !1}}
                    }
                })
            }
            let c = [t.voltage_phase_1, t.voltage_phase_2, t.voltage_phase_3];
            if (r) r.data.datasets[0].data = c, r.update(); else {
                let u = document.getElementById("voltagePhaseChart").getContext("2d");
                r = new Chart(u, {
                    type: "line",
                    data: {
                        labels: ["Phase 1 (V)", "Phase 2 (V)", "Phase 3 (V)"],
                        datasets: [{
                            label: "Voltage Phase",
                            data: c,
                            borderColor: "#ff9900",
                            backgroundColor: "rgba(255, 153, 0, 0.2)",
                            borderWidth: 3,
                            pointRadius: 5,
                            pointBackgroundColor: "#ff6600",
                            fill: !0
                        }]
                    },
                    options: {
                        responsive: !0,
                        maintainAspectRatio: !1,
                        plugins: {legend: {display: !0, position: "top"}},
                        scales: {x: {grid: {display: !1}}, y: {grid: {borderDash: [5, 5]}}}
                    }
                })
            }
            let g = [t.current_phase_1, t.current_phase_2, t.current_phase_3];
            if (l) l.data.datasets[0].data = g, l.update(); else {
                let h = document.getElementById("currentMetricsChart").getContext("2d");
                l = new Chart(h, {
                    type: "doughnut",
                    data: {
                        labels: ["Current Phase 1 (A)", "Current Phase 2 (A)", "Current Phase 3 (A)"],
                        datasets: [{
                            label: "Current & Other Metrics",
                            data: g,
                            backgroundColor: ["#1abc9c", "#3498db", "#f1c40f"],
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: !0,
                        maintainAspectRatio: !1,
                        plugins: {legend: {display: !0, position: "right", labels: {boxWidth: 20, padding: 10}}}
                    }
                })
            }
        })(e)).catch(e => console.error("Error fetching solar data:", e))
    }, 5e3)
});