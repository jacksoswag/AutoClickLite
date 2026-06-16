# autoclicker

A minimal command-line autoclicker for the mouse, written in Python with [`pynput`](https://pypi.org/project/pynput/).

## Overview

`autoclicker.py` prompts for a click rate, then runs a background thread that
clicks the left mouse button at that rate whenever clicking is toggled on. A
global keyboard listener lets you start and stop clicking with a hotkey without
returning focus to the terminal. The clicker keeps running until you stop the
process.

## Features

- Configurable click rate, entered as clicks per second at startup.
- Background click loop on a daemon thread, so the keyboard listener stays responsive.
- Global hotkey to toggle clicking on and off from anywhere.
- Self-correcting timing: each cycle subtracts the time the click took from the
  sleep interval to keep the rate close to the target.

## Requirements

- Python 3
- [`pynput`](https://pypi.org/project/pynput/)

On macOS, `pynput` needs Accessibility (and, for the keyboard listener, Input
Monitoring) permission. Grant the terminal app you run this from access under
**System Settings -> Privacy & Security**, or the click and key events will be
silently ignored.

## Install

```bash
pip install pynput
```

## Usage

```bash
python autoclicker.py
```

1. Enter the desired clicks per second when prompted (for example, `10`).
   Fractional values are accepted (for example, `0.5` for one click every two
   seconds).
2. Press the toggle key to start clicking; press it again to stop. The terminal
   prints `Clicking started` / `Clicking stopped` on each toggle.
3. Stop the program with `Ctrl+C`.

### Toggle key

The toggle is bound to the `x` and `,` keys. Pressing either one flips clicking
on or off.

> Note: the on-screen prompt currently reads `Press ',' or '.'`, but the
> handler actually listens for `x` and `,`. Use `x` or `,`.

The hotkey is captured globally, so it fires even when the terminal is not the
focused window. Keep that in mind, since the toggle keys also type normally into
other applications.

## How it works

- `mouse.Controller()` issues the actual left clicks.
- `click_loop()` runs on a daemon thread. While the `clicking` flag is true it
  clicks once per interval (`1 / n` seconds); while false it idles in a short
  sleep.
- `keyboard.Listener` runs the `on_press` handler, which toggles the shared
  `clicking` flag when the bound key is pressed.

## Development notes

- Single file, no build step, no external config.
- State is shared through the module-level `clicking` flag between the listener
  and the click thread.
- The click rate is fixed at startup; to change it, restart the program.

## Status

Working prototype / personal utility. Single-file script with no packaging,
tests, or CLI argument parsing.
