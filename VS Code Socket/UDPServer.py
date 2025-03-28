"""
Program Name: UDPServer.py
Description: This program implements a simple UDP server that listens for messages from clients,
             converts the received messages to uppercase, and sends the modified messages back
             to the clients.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to start the UDP server.
    2. The server will listen on the specified port for incoming messages from clients.
    3. When a message is received, the server will process it and send the response back to the client.

Requirements:
    - Python 3.x
    - The `socket` library for UDP communication.

Notes:
    - The server listens on all available network interfaces (IP address `''`) and the specified port.
    - The port number can be modified in the `serverPort` variable.
    - This program runs indefinitely until manually stopped.

"""

from socket import *    # Import socket library

serverPort = 12000  # Server port number
serverSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
serverSocket.bind(('', serverPort)) # Bind the socket to the server address and port
print('The server is ready to receive') # Print a message indicating the server is ready

while True:   # Infinite loop to keep the server running
    message, clientAddress = serverSocket.recvfrom(2048)    # Receive message from client
    modifiedMessage = message.decode().upper()  # Convert the message to uppercase
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)    # Send the modified message back to the client

