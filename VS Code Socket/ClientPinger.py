"""
Program Name: ClientPinger.py
Description: This program implements a simple UDP client that sends "PING" messages to a server
             and waits for "PONG" responses. It calculates and displays the Round Trip Time (RTT)
             for each message and reports packet loss if no response is received within a timeout.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Ensure the UDP server is running and listening on the specified host and port.
    2. Run this program to send "PING" messages to the server.
    3. The program will display the server's responses and the RTT for each message.

Requirements:
    - Python 3.x
    - The `socket` library for UDP communication.

Notes:
    - The server's host and port can be modified in the `ping_server` function call.
    - The program sends 10 "PING" messages to the server, one per second.
    - If no response is received within 1 second, the program assumes packet loss.
"""

import socket   # Import socket library
import time # Import time library for timing operations

def ping_server(host, port):    # Function to send ping messages to the server
    # Create a UDP socket
    try:    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Create a UDP socket
    except socket.error as e:   # Handle socket creation error
        print(f"Error creating socket: {e}")
        return
    with client_socket:     # Use the socket in a context manager to ensure it is closed properly
        client_socket.settimeout(1)  # Set a timeout of 1 second
        for i in range(10):   # Send 10 ping messages
            message = f"PING {i+1}".encode()  # Ping message
            start_time = time.time()  # Record the time before sending the message
            
            # Send the ping message to the server
            client_socket.sendto(message, (host, port))
            print(f"Sent: {message.decode()}")
            
            try:
                # Wait for a reply (pong) from the server
                data, server = client_socket.recvfrom(1024)
                end_time = time.time()  # Record the time after receiving the reply

                # Calculate Round Trip Time (RTT)
                rtt = (end_time - start_time) * 1000  # Convert RTT to milliseconds
                print(f"Received: {data.decode()} | RTT = {rtt:.2f} ms")
            
            except socket.timeout:
                # If no reply within 1 second, assume packet loss
                print(f"Request {i+1} timed out. Packet lost.")

if __name__ == "__main__":
    # Client sending pings to localhost on port 12345
    ping_server("10.0.0.199", 12000)
