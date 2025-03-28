"""
Program Name: TCPServer.py
Description: This program implements a simple TCP server that listens for client connections,
             receives messages, processes them by converting to uppercase, and sends the
             modified messages back to the clients. It demonstrates basic TCP socket programming
             in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to start the TCP server.
    2. The server will listen on the specified port for incoming client connections.
    3. When a client sends a message, the server will process it and send the response back.

Requirements:
    - Python 3.x
    - The `socket` library for TCP communication.

Notes:
    - The server listens on all available network interfaces (IP address `''`) and the specified port.
    - The port number can be modified in the `serverPort` variable.
    - This program runs indefinitely until manually stopped.
"""

from socket import *    # Import socket library

serverPort = 12000  # Server port number
serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
serverSocket.bind(('', serverPort)) # Bind the socket to the server address and port
serverSocket.listen(1)  # Listen for incoming connections

print('The server is ready to receive') # Print a message indicating the server is ready

while True:  # Infinite loop to keep the server running 
    connectionSocket, addr = serverSocket.accept()  # Accept a connection from a client
    sentence = connectionSocket.recv(1024).decode() # Receive message from client
    capitalizedSentence = sentence.upper()      # Convert the message to uppercase
    connectionSocket.send(capitalizedSentence.encode()) # Send the modified message back to the client
    connectionSocket.close()    # Close the connection with the client
