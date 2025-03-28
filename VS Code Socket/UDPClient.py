"""
Program Name: UDPClient.py
Description: This program sends a message to a UDP server and receives a response. 
             It demonstrates basic UDP socket programming in Python.
             
Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage: 
    1. Ensure the UDP server is running and listening on the specified IP and port.
    2. Run this program and input a message when prompted.
    3. The program will send the message to the server and display the server's response.

Requirements:
    - Python 3.x
    - A running UDP server on the specified IP and port.

Notes:
    - This program uses the `socket` library for UDP communication.
    - The server IP and port can be modified in the `serverName` and `serverPort` variables.

"""

# Program to send a message to a UDP server and receive a response
from socket import *    # Import socket library

serverName = '10.0.0.140'   # Server IP address
serverPort = 12000  # Server port number
clientSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
message = input('Input lowercase sentence:')    # Prompt user for input
clientSocket.sendto(message.encode(), (serverName, serverPort)) # Send message to server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)    # Receive response from server
print(modifiedMessage.decode())   # Print the server's response
clientSocket.close()    # Close the socket
