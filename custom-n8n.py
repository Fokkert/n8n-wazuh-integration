#!/usr/bin/env python3

# Importing Packages
import sys
import json
import requests
import urllib3
import traceback

# Disable SSL certificate warnings ( Comment out if you have a valid certificate )
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Hard-coded token for webhook authentication
WEBHOOK_AUTH_TOKEN = "<Your-Authentication-Token>" # Comment out if you are not using authentication for your webhook

# Args from Wazuh
alert_file = sys.argv[1]
hook_url = sys.argv[3]

# Load full Wazuh alert JSON
try:
    with open(alert_file, "r") as f:
        alert_json = json.loads(f.read())
except Exception as e:
    print(f"[ERROR] Failed to read alert file: {e}")
    traceback.print_exc()
    sys.exit(1)

# Prepare payload — Untouched full alert
payload = {
    "wazuh_alert": alert_json
}

# Build headers with hard-coded token
headers = {
    "content-type": "application/json",
    "Wazuh-Webhook-Auth-Token": WEBHOOK_AUTH_TOKEN # Comment out if you are not using authentication for your webhook
}

# Send request
try:
    r = requests.post(
        hook_url,
        json=payload,
        headers=headers,
        verify=False
    )
    r.raise_for_status()
    print(f"[INFO] Alert sent to {hook_url}, status_code={r.status_code}")
except Exception as e:
    print("[ERROR] Failed to send alert:")
    traceback.print_exc()
    try:
        with open("/var/ossec/logs/integration.log", "a") as log:
            log.write(f"Error sending alert to {hook_url}: {str(e)}\n")
            log.write(f"Headers: {json.dumps(headers)}\n")
            log.write(f"Payload:\n{json.dumps(payload, indent=2)}\n")
            log.write(f"Traceback:\n{traceback.format_exc()}\n")
    except Exception as log_err:
        print(f"[ERROR] Failed to write to integration.log: {log_err}")
    sys.exit(1)
