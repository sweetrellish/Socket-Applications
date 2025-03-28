"""
Program Name: WebServer.py
Description: This program implements a simple HTTP web server that listens for client requests,
             serves static files, and returns appropriate HTTP responses. It demonstrates basic
             socket programming and HTTP protocol handling in Python.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to start the web server.
    2. The server will listen on the specified host and port for incoming HTTP requests.
    3. Clients can connect to the server using a web browser or an HTTP client (e.g., curl).
    4. The server will serve static files from the current working directory.

Requirements:
    - Python 3.x
    - The `socket` and `os` libraries for network communication and file handling.

Notes:
    - The server listens on the specified host and port defined in the `HOST` and `PORT` variables.
    - The server only serves files from the current working directory.
    - If a requested file is not found, the server returns a 404 Not Found response.
    - This program is for educational purposes and is not intended for production use.
"""

import socket
import os

# Define the server's host and port
HOST = 'localhost'
PORT = 8080

def handle_request(client_socket):
    # Receive the HTTP request
    request = client_socket.recv(1024).decode('utf-8')

    if not request:
        client_socket.close()
        return

    # Print the request to see what the client requested
    print("Request received:")
    print(request)

    # Parse the request to determine the file requested
    lines = request.splitlines()
    if len(lines) > 0:
        # Extract the requested file (second element in the request line)
        requested_file = lines[0].split()[1][1:]  # Remove leading '/' from the path

        # Check if the file exists on the server
        if os.path.exists(requested_file) and os.path.isfile(requested_file):
            # If the file exists, open it and send it as a response
            with open(requested_file, 'rb') as file:
                content = file.read()

            # Create the HTTP response headers and body
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type: text/html\r\n"
            response_headers += "Content-Length: " + str(len(content)) + "\r\n"
            response_headers += "\r\n"  # End of headers

            # Send the response
            client_socket.sendall(response_headers.encode('utf-8'))
            client_socket.sendall(content)
        else:
            # If the file doesn't exist, return a 404 Not Found response
            response_headers = "HTTP/1.1 404 Not Found\r\n"
            response_headers += "Content-Type: text/html\r\n"
            response_headers += "\r\n"  # End of headers

            # Create a simple HTML message for 404
            response_body = "<html><body><h1>404 Not Found</h1><p>The requested file could not be found.</p></body></html>"

            # Send the response
            client_socket.sendall(response_headers.encode('utf-8'))
            client_socket.sendall(response_body.encode('utf-8'))
    
    # Close the client connection
    client_socket.close()

def start_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)  # Listen for incoming connections (1 client at a time)

        print(f"Server listening on {HOST}:{PORT}...")

        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()

        print(f"Connection from {client_address}")

        # Handle the client request
        handle_request(client_socket)

if __name__ == "__main__":
    start_server()
