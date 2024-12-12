# ZTE_watchdog

### Requirements
```
python -m pip install requests js2py
```

### Description
This application monitors internet connectivity by periodically pinging Google's DNS server (8.8.8.8). If the ping fails, it performs the following actions:
1. Attempts to reconnect by retrying the ping up to 5 times.
2. If all retry attempts fail, it reboots the specified router (either ZTE-Modem or OpenWrt).

### Usage

#### Command-Line Arguments
The script requires several parameters to function correctly. These parameters allow you to specify the IP address and credentials of the ZTE-Modem and OpenWrt router. Run the script as follows:

```bash
python3 zte_watchdog.py --zte_ip <ZTE_IP> --zte_password <ZTE_PASSWORD> --openwrt_ip <OPENWRT_IP> --openwrt_user <OPENWRT_USER> --openwrt_password <OPENWRT_PASSWORD>
```

**Arguments:**
- `--zte_ip`: IP address of the ZTE-Modem.
- `--zte_password`: Password for the ZTE-Modem.
- `--openwrt_ip`: IP address of the OpenWrt router.
- `--openwrt_user`: Username for the OpenWrt router.
- `--openwrt_password`: Password for the OpenWrt router.

### Service Definition
You can configure the script to run as a Linux service for continuous monitoring. This ensures the script starts at boot and automatically restarts if it crashes.

#### Create the Service File
Create a systemd service file at `/etc/systemd/system/zte_watchdog.service` with the following content:

```ini
[Unit]
Description=Internet Connectivity Watchdog and Router Reboot Service
Documentation=Monitors internet connectivity by pinging Google every 10 seconds. If connectivity fails, attempts additional pings. After 5 failures, reboots the specified router (ZTE or OpenWrt).

[Service]
ExecStart=/usr/bin/python3 /path/to/zte_watchdog.py --zte_ip <ZTE_IP> --zte_password <ZTE_PASSWORD> --openwrt_ip <OPENWRT_IP> --openwrt_user <OPENWRT_USER> --openwrt_password <OPENWRT_PASSWORD>
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/zte_watchdog.py` with the actual path to the script and substitute `<ZTE_IP>`, `<ZTE_PASSWORD>`, `<OPENWRT_IP>`, `<OPENWRT_USER>`, and `<OPENWRT_PASSWORD>` with the appropriate values.

#### Enable and Start the Service
1. Reload the systemd daemon to recognize the new service:
   ```bash
   sudo systemctl daemon-reload
   ```

2. Enable the service to start at boot:
   ```bash
   sudo systemctl enable zte_watchdog.service
   ```

3. Start the service:
   ```bash
   sudo systemctl start zte_watchdog.service
   ```

4. Check the status of the service:
   ```bash
   sudo systemctl status zte_watchdog.service
   ```

### Notes
- Ensure `sshpass` is installed on your system for OpenWrt router reboots.
- The script assumes root-level privileges to execute router reboots. Ensure the service is properly secured to avoid unauthorized access.
- Logs can be viewed using `journalctl -u zte_watchdog.service`.
