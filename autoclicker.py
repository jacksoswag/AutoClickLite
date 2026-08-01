"""Minimal command-line autoclicker: toggles rapid left-clicks with a global hotkey."""

import threading
import time
from pynput import mouse, keyboard

# --- SETTINGS ---
def read_clicks_per_second():
    while True:
        try:
            value = float(input("Enter clicks per second (n): "))
        except ValueError:
            print("Please enter a number.")
            continue
        if value <= 0:
            print("Please enter a number greater than 0.")
            continue
        return value

try:
    n = read_clicks_per_second()
except (EOFError, KeyboardInterrupt):
    print()
    raise SystemExit(0)

interval = 1 / n
clicking = False

# --- MOUSE CONTROLLER ---
mouse_controller = mouse.Controller()

# --- CLICK FUNCTION ---
def mouse_click():
    mouse_controller.click(mouse.Button.left, 1)

# --- CLICK LOOP ---
def click_loop():
    global clicking
    while True:
        if clicking:
            start = time.perf_counter()
            mouse_click()
            elapsed = time.perf_counter() - start
            time.sleep(max(0, interval - elapsed))
        else:
            time.sleep(0.05)

# --- HOTKEYS ---
def on_press(key):
    global clicking
    try:
        if key.char in ['x', ',']:
            clicking = not clicking
            print("Clicking started" if clicking else "Clicking stopped")
    except AttributeError:
        pass

# --- START THREAD ---
thread = threading.Thread(target=click_loop, daemon=True)
thread.start()

print("Press 'x' or ',' to start/stop clicking (runs continuously).")
print("Press Ctrl-C to quit.")

try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\nStopped.")