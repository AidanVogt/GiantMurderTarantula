import pygame
import time
import json
import os
import urllib.error
import urllib.request

# EVENTUAL CODE FOR RASPBERRY PI

# init a joystick 
pygame.init()
pygame.joystick.init()


# check
if pygame.joystick.get_count() == 0:
    print("no controller")
    exit(1)

# start
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller: {joystick.get_name()}")

SERVER_URL = os.getenv("JOYSTICK_SERVER_URL", "http://127.0.0.1:5000")
config = {
    "deadzone": 0.08,
    "invert_y": True,
    "telemetry_hz": 30,
}
last_cfg_pull = 0.0


def apply_deadzone(value, dz):
    if abs(value) < dz:
        return 0.0
    return value


def fetch_config():
    global config
    try:
        with urllib.request.urlopen(f"{SERVER_URL}/api/config", timeout=0.2) as resp:
            body = resp.read().decode("utf-8")
            new_cfg = json.loads(body)
            if isinstance(new_cfg, dict):
                config.update(new_cfg)
    except Exception:
        # Keep current config if server is unavailable.
        pass


def post_telemetry(axes, buttons):
    payload = json.dumps({"axes": axes, "buttons": buttons}).encode("utf-8")
    req = urllib.request.Request(
        f"{SERVER_URL}/api/telemetry",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=0.2):
            return
    except urllib.error.URLError:
        return


while True:
    now = time.time()
    if now - last_cfg_pull > 1.0:
        fetch_config()
        last_cfg_pull = now

    pygame.event.pump()
    
    # read joystick axes (typically 0=left X, 1=left Y, 2=right X, 3=right Y)
    left_x = joystick.get_axis(0)
    left_y = joystick.get_axis(1)
    right_x = joystick.get_axis(2)
    right_y = joystick.get_axis(3)

    if config.get("invert_y", True):
        left_y = -left_y
        right_y = -right_y

    dz = float(config.get("deadzone", 0.08))
    left_x = apply_deadzone(left_x, dz)
    left_y = apply_deadzone(left_y, dz)
    right_x = apply_deadzone(right_x, dz)
    right_y = apply_deadzone(right_y, dz)

    pressed_buttons = [
        i for i in range(joystick.get_numbuttons()) if joystick.get_button(i)
    ]
    axes = {
        "left_x": left_x,
        "left_y": left_y,
        "right_x": right_x,
        "right_y": right_y,
    }
    post_telemetry(axes, pressed_buttons)

    print(f"\rLeft: ({left_x:6.2f}, {left_y:6.2f})  |  Right: ({right_x:6.2f}, {right_y:6.2f})", end="")

    hz = max(1, int(config.get("telemetry_hz", 30)))
    time.sleep(1.0 / hz)
