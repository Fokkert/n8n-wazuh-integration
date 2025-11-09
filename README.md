# n8n - Wazuh Integration Guide

This repository contains files & documents which help you integrate n8n and Wazuh in order to receive wazuh alerts in your n8n workflows. This helps you automate notifications , responses and documentations based on the alerts and never miss one. Wazuh is an Open-Source SIEM and XDR platform with numerous capabilities while n8n , is another Open-Source platform used by many Developers and IT technicians for automating IT procedures or daily tasks.

## Configuring n8n

First , you need to create a workflow in your n8n instance. you can name it whatever you want. after creating the workflow you must create a trigger node inside the workflow. The type of the trigger node must be Webhook. from the node you can extract many information needed for the rest of the configurations. Change the path of the webhook if you want a clean URL. If you want to enable authentication for a secure integration , Enable Authentication in the n8n Webhook node with the "Header Auth" type. then create a Credential for that. in the Credential , you must pay attention to the Name and Value you set for the header as we need them later in our python script. Remember to change the HTTP Method to "POST" if it is not already like that. After that, save the workflow and proceed to the next part of the guide.

## Configuring Wazuh

After configuring n8n for the integration , we need to start configuring our Wazuh servers. You MUST apply all these changes to all of the members of your Wazuh Server cluster no matter if it is the master or any of the workers. first , put the custom-n8n file which is in this repository in /var/ossec/integrations/  with the exact same name. you can rename the file to anything you want but you must keep the "custom-" part. after that , put the custom-n8n.py file inside the same path with the exact same name that you used for the first script. the only difference must be the suffix which is not used for the first script and is ".py" for the second one. Now , you must edit the custom-n8n.py script ( or whatever you named it ). There are 2 parts in the script that you must change based on if you have enabled Authentication in the n8n node or not. If you have not enabled Authentication , either comment out or completely remove these 2 parts in the script :

```
WEBHOOK_AUTH_TOKEN = "<Your-Authentication-Token>"
```
```
headers = {
    "content-type": "application/json",
    "Wazuh-Webhook-Auth-Token": WEBHOOK_AUTH_TOKEN # Comment out if you are not using authentication for your webhook
}
```

Otherwise , replace <Your-Authentication-Token> with the Value you set in the credential in n8n , and replace "Wazuh-Webhook-Auth-Token" with the name you gave the Credential in n8n. In addition to that , if you have a valid certificate for your n8n instance , comment out this part completely :

```
# Disable SSL certificate warnings ( Comment out if you have a valid certificate )
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

Otherwise , just keep it.

### Modifying ossec.conf

After completing the previous steps , you must edit your Wazuh Server configuration to use the following scripts for sending the alerts. For that , open /var/ossec/etc/ossec.conf and find a good spot in the <ossec_config></ossec_config> tag and put this tag inside it :

```
  <integration>
    <name>custom-n8n</name>
    <hook_url>[Your-Webhook-URL]</hook_url>
    <alert_format>json</alert_format>
  </integration>
```

Replace [Your-Webhook-URL] with the URL you have in your n8n Webhook node and also , if you have changed the name of the scripts in the previous steps , modify the <name></name> tag and replace the value with the name you chose for the scripts.

### Restarting The Services

