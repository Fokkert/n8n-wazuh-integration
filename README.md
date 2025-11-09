# n8n - Wazuh Integration Guide

This repository contains files & documents which help you integrate n8n and Wazuh in order to receive wazuh alerts in your n8n workflows. This helps you automate notifications , responses and documentations based on the alerts and never miss one. Wazuh is an Open-Source SIEM and XDR platform with numerous capabilities while n8n , is another Open-Source platform used by many Developers and IT technicians for automating IT procedures or daily tasks.


## Getting Started

First , you need to create a workflow in your n8n instance. you can name it whatever you want. after creating the workflow you must create a trigger node inside the workflow. The type of the trigger node must be Webhook. from the node you can extract many information needed for the rest of the configurations. Change the path of the webhook if you want a clean URL. 
