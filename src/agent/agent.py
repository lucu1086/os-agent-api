# ---Agent.py---
# This file is part of the Agent project.
# It is subject to the license terms in the LICENSE file found in the top-level directory of this distribution.
# The full list of contributors can be found in the AUTHORS file in the same directory.
# This script collects system information and sends it to a specified API endpoint.
# This collects data such as CPU usage, running processes, logged-in users, and OS information.
# Multiple platforms are supported, including Linux, Windows, and macOS.

import psutil
import requests
import platform
import json
import socket
import os

# API endpoint for sending data
# Replace with your actual API endpoint

API_ENDPOINT = "https://example.com/api/agent_data"
API_TOKEN = os.getenv("API_TOKEN")  # Get API token from environment variable



# Function to collect system information
def collect_system_info():
    # Information about CPU
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None,
        "current_frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        "cpu_usage_percent": psutil.cpu_percent(interval=1)
    }

    # List of running processes
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Users currently logged in
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": user.started
        })

    # Operating system information
    os_info = {
        "system": platform.system(),
        "version": platform.version(),
        "hostname": socket.gethostname()
    }

    system_info = {
        "cpu_info": cpu_info,
        "processes": processes,
        "users": users,
        "os_info": os_info
    }
    return system_info
    # Send collected data to the API
def send_data_to_api(data):
    if not API_TOKEN:
        print("Error: API_TOKEN no está definida en las variables de entorno.")
        return
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    try:
        response = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print("Datos enviados correctamente.")
    except requests.RequestException as e:
        print(f"Error al enviar datos: {e}")

if __name__ == "__main__":
    info = collect_system_info()
    send_data_to_api(info)
