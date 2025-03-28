"""
Program Name: TCPClient.py
Description: This program implements a simple TCP client that connects to a TCP server,
             sends a message, and receives a response. It demonstrates basic TCP socket
             programming in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Ensure the TCP server is running and listening on the specified IP and port.
    2. Run this program and input a message when prompted.
    3. The program will send the message to the server and display the server's response.

Requirements:
    - Python 3.x
    - A running TCP server on the specified IP and port.

Notes:
    - The server IP and port can be modified in the `serverName` and `serverPort` variables.
    - This program demonstrates a simple request-response interaction over TCP.
"""

from socket import *    # Import socket library

serverName = 'hostname' # Server IP address (replace with actual server IP)
serverPort = 12000  # Server port number
clientSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
clientSocket.connect((serverName, serverPort))  # Connect to the server
sentence = input('Input lowercase sentence:')   # Prompt user for input
clientSocket.send(sentence.encode())    # Send message to server
modifiedSentence = clientSocket.recv(1024)  # Receive response from server
print('From Server:', modifiedSentence.decode())    # Print the server's response
clientSocket.close()
# Close the socket