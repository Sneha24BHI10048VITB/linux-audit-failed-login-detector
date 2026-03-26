# linux-audit-failed-login-detector
# Failed Login Attempt Monitor Notifications

This Python script monitors for failed login attempts on your Linux system using the `lastb` command and sends real-time notifications via Gotify, Email and ntfy when a new failed login is detected.

## Features

* **Real-time monitoring:** Detects and notifies you of new failed login attempts as they occur.
* **Notifications:**  Sends clear and concise notifications to your Gotify-enabled devices, email, and ntfy .
* **Efficient:** Checks for new failed logins periodically to avoid excessive resource usage.

## Prerequisites

* **Linux system with `lastb`:**  Ensure that the `lastb` command is available on your system (commonly found on Linux distributions).
* **Python 3:**  The script requires Python 3 to be installed.
* **Gotify server and app:** If using Gotify, set up a Gotify server and create an app to obtain the necessary URL and token.
* **Email:** If using email it is recommended to use an app password.
* **Ntfy:** You can use ntfy default servers or setup your own..

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Editz7/Realtime-Failed-Login
   cd Realtime-Failed-Login

2. **Configure the script**
   Open `config.ini` and configure to your liking.

## Usage

1. **Run the script:**
   Must be ran as ``sudo`` because of ``lastb`` command.
   ```bash
   sudo python main.py

2. **Monitor for notifications:**
   The script will run in the background and send notifications whenever a new failed login attempt is detected. Test this by doing a failed login on your system.

### Road Map
- [x] Ntfy Notifications
- [x] Gotify Notifications
- [x] Email Notifications
- [ ] Telegram Notifications
- [ ] Fix to fully show IP on notification
