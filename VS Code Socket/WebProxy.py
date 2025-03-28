"""
Program Name: WebProxy.py
Description: This program implements a simple HTTP proxy server that listens for client requests,
             forwards them to the destination server, and relays the responses back to the client.
             It demonstrates basic socket programming and multithreading in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to start the proxy server.
    2. The proxy server will listen on the specified host and port for incoming HTTP requests.
    3. Clients can configure their browser or HTTP client to use this proxy server.
    4. The proxy server will forward client requests to the destination server and return the responses.

Requirements:
    - Python 3.x
    - The `socket` and `threading` libraries for network communication and multithreading.

Notes:
    - The proxy server listens on the specified host and port defined in the `startProxyServer` function.
    - This program is for educational purposes and is not intended for production use.
    - The proxy server does not support HTTPS or advanced HTTP features.
"""

import socket   # Import socket library
import sys  # Import sys library for command-line arguments
import threading    # Import threading library for multithreading

#Function to handle the client connection
def handleClient(clientSocket):
    try:
        #Receive the HTTP request from the client
        request = clientSocket.recv(1024).decode()

        #Print the HTTP request (for debugging)
        print(f"Request received:\n{request}")

        #Parse the HTTP request to extract destination host and path
        lines = request.split("\r\n")
        url = lines[0].split(" ")[1] #get URL from first line

        #Extract the domain from the URL 
        host = url.split("//")[1].split("/")[0]
        port = 80 #default HTTP port

        #Create a socket to communicate with origin server
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.connect((host, port))

        #Forward the HTTP request to the origin server
        serverSocket.send(request.encode())

        #Receive the response from the origin server
        response = serverSocket.recv(4096)

        #Send the response back to the client
        clientSocket.send(response)

        #close the sockets
        serverSocket.close()
        clientSocket.close()

    except Exception as e:
        print(f"Error handling client: {e}")
        clientSocket.close()

def startProxyServer(host = 'localhost', port = 8080):
    #Create a TCP socket for the proxy server
    proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxySocket.bind((host, port))
    proxySocket.listen(5)

    print(f"Proxy server listening on {host}:{port}")

    while True:
        #Accept a client connection
        clientSocket, addr = proxySocket.accept()
        print(f"Accepted connection from {addr}")

        #Handle the client connection in a separate thread
        clientThread = threading.Thread(target=handleClient, args=(clientSocket,))
        clientThread.start()

#Entry point for the script
if __name__ == "__main__":
    #Start the proxy server on the default host and port
    startProxyServer()

    