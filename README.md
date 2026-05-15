# LinkedIn Activity Tracker

An undetectable LinkedIn activity tracker using Scrapling and Chromium. It tracks the absolute latest activity (posts, comments, or reposts) with millisecond precision by decoding LinkedIn URNs.

## 🚀 Quick Start

### 1. Initial Setup
Run the following command to create a virtual environment, install dependencies, and download browsers:
```bash
./setup.sh
```

### 2. Manual Login (One-Time)
You must perform a manual login once so the browser can save your cookies and session data locally.
```bash
./venv/bin/python3 open_browser.py
```
*A browser window will open. Log in to LinkedIn, then close the window.*

### 3. Track a Profile
Run the tracker with any LinkedIn profile URL. It will output the latest activity as JSON.
```bash
./venv/bin/python3 linkedin_tracker.py "https://www.linkedin.com/in/username"
```

## 🛠 Features
- **Persistent Sessions**: Cookies and cache are saved in `.scrapling_session/`, persisting across restarts.
- **Anti-Bot Detection**: Uses Scrapling's stealth engine to bypass protections.
- **Precise Timestamps**: Decodes `data-urn` attributes to get the exact millisecond of the activity.
- **Unified Tracking**: Checks 'All', 'Posts', and 'Comments' sections automatically.

## 📦 Project Structure
- `Scrapling/`: The modified Scrapling library.
- `linkedin_tracker.py`: The main automation script.
- `open_browser.py`: Helper script for manual login.
- `setup.sh`: Automated environment setup.
- `.scrapling_session/`: (Generated) Stores your persistent browser data.
