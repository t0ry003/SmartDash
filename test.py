import requests

DEVICE_IP = "192.168.0.140"  # replace if needed
TOGGLE_URL = f"http://{DEVICE_IP}/toggle"


def toggle_relay(state):
    if state not in ["on", "off"]:
        print("Invalid state. Use 'on' or 'off'.")
        return

    headers = {"Content-Type": "application/json"}
    payload = {"state": state}

    try:
        response = requests.post(TOGGLE_URL, headers=headers, json=payload)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


# Test usage
toggle_relay("off")
# toggle_relay("off")  # uncomment to test "off"
