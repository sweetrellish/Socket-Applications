#!/bin/bash
# Launch Browser in Firejail Sandbox
BROWSER="firefox" # Replace with your browser of choice
echo "[+] Launching $BROWSER in sandbox..."
firejail --noprofile --seccomp --caps.drop=all $BROWSER --private-window
if [ $? -eq 0 ]; then
    echo "[+] Browser launched securely."
else
    echo "[!] Failed to launch browser. Ensure firejail is installed."
    exit 1
fi
