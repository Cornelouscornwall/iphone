#!/usr/bin/env python3
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = "file://" + os.path.join(ROOT, "index.html")


def open_in_browser(url):
    candidates = [
        "google-chrome",
        "chromium",
        "chromium-browser",
        "google-chrome-stable",
        "xdg-open",
    ]
    for cmd in candidates:
        try:
            if cmd == "xdg-open":
                subprocess.Popen([cmd, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([cmd, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            continue
    return False


def main():
    print(f"Opening VPN portal: {INDEX}")
    if not open_in_browser(INDEX):
        print("No browser found. Open index.html manually in Chrome.")


if __name__ == "__main__":
    main()
    sys.exit(0)
