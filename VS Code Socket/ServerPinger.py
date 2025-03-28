"""
Program Name: ServerPinger.py
Description: This program implements a simple UDP server that listens for "ping" messages from clients
             and responds with a "PONG" message. It demonstrates basic UDP socket programming in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to start the UDP server.
    2. The server will listen on the specified host and port for incoming "ping" messages.
    3. When a "ping" message is received, the server will respond with a "PONG" message.

Requirements:
    - Python 3.x
    - The `socket` library for UDP communication.

Notes:
    - The server listens on the specified host and port defined in the `host` and `port` variables.
    - This program runs indefinitely until manually stopped.
    - Ensure the client program is configured to send messages to the correct host and port.
"""

import socket   # Import socket library

def start_server(host, port):   # Function to start the UDP server
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:     
        server_socket.bind((host, port))    # Bind the socket to the specified host and port
        print(f"Server listening on {host}:{port}...")  # Print a message indicating the server is ready
        
        while True:
            # Wait for a message from the client
            message, client_address = server_socket.recvfrom(1024)
            print(f"Received ping from {client_address}: {message.decode()}")

            # Send back a pong message to the client
            server_socket.sendto(b"PONG", client_address)

if __name__ == "__main__":
    # Server listening on localhost and port 12345
    start_server("10.0.0.199", 12000)
