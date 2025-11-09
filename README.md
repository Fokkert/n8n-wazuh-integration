# n8n – Wazuh Integration Guide

This repository contains files and documentation to help you integrate **n8n** and **Wazuh**, enabling you to receive Wazuh alerts directly in your n8n workflows. This integration allows you to automate notifications, responses, and documentation based on Wazuh alerts—ensuring you never miss one.

**Wazuh** is an open-source SIEM and XDR platform with numerous capabilities.  
**n8n** is another open-source automation platform used by many developers and IT technicians to automate IT procedures and daily tasks.

## 1. Configuring n8n

1. First, create a new **workflow** in your n8n instance (you can name it whatever you want).
2. Inside the workflow, create a **Webhook trigger node**.
3. Adjust the **path** of the webhook if you want a clean URL.
4. If you want secure integration, enable **Authentication** in the n8n Webhook node using the `"Header Auth"` type.
5. Create a **Credential** for authentication.  
   - Pay attention to the **Name** and **Value** you set for the header, as they will be needed later in the Python script.
6. Change the HTTP Method to **POST** if it’s not already set.
7. Save the workflow and proceed to Wazuh configuration.

## 2. Configuring Wazuh

After setting up n8n, configure your Wazuh servers.  
You **must** apply these changes to **all members** of your Wazuh Server cluster (both master and workers).

1. Place the file `custom-n8n` from this repository into:

```plaintext
/var/ossec/integrations/
```

2. Rename the file only if you wish, but keep the `"custom-"` prefix.
3. Place the file `custom-n8n.py` into the same directory:

```plaintext
/var/ossec/integrations/
```

4. The `.py` file must match the name you used for the first script (with `.py` as the suffix).
5. Edit the `custom-n8n.py` script as follows:

   - If **Authentication is disabled** in your n8n Webhook node, comment out or remove these lines ( keep `"content-type": "application/json"` ) :

```python
WEBHOOK_AUTH_TOKEN = "<Your-Authentication-Token>"
```

```python
headers = {
    "content-type": "application/json",
    "Wazuh-Webhook-Auth-Token": WEBHOOK_AUTH_TOKEN  # Comment out if not using authentication
}
```

   - If **Authentication is enabled**, replace `<Your-Authentication-Token>` with the **Value** you set in n8n credentials, and replace `"Wazuh-Webhook-Auth-Token"` with the **Credential Name** used in n8n.

6. If your n8n instance has a valid SSL certificate, comment out or remove this line completely:

```python
# Disable SSL certificate warnings (comment out if you have a valid certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

   Otherwise, leave it as is.

## 3. Modifying `ossec.conf`

Edit the Wazuh Server configuration to use your custom integration script:

1. Open:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

2. Inside the `<ossec_config>` tag, insert:

```xml
<integration>
  <name>custom-n8n</name>
  <hook_url>[Your-Webhook-URL]</hook_url>
  <alert_format>json</alert_format>
</integration>
```

3. Replace `[Your-Webhook-URL]` with the Webhook URL from your n8n Webhook node.
4. If you renamed the scripts earlier, update the `<name>` tag accordingly.

## 4. Restarting Wazuh Manager

Restart the Wazuh Manager service to apply changes:

```bash
sudo systemctl restart wazuh-manager
```

### Debugging The Integration

You can check `/var/ossec/logs/integrations.log` to find any errors or alerts that could potentially interrupt your integration.


✅ **You’re all set! , Just wait for the first alert and then extend your workflow based on that !**  
