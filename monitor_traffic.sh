#!/bin/bash
# Monitor Network Traffic

INTERFACE="eth0" # Replace with your interface name
echo "[+] Monitoring traffic on $INTERFACE..."
sudo tcpdump -i $INTERFACE -n -c 100
if [ $? -eq 0 ]; then
    echo "[+] Traffic monitoring complete."
else
    echo "[!] Failed to monitor traffic. Ensure tcpdump is installed."
    exit 1
fi
