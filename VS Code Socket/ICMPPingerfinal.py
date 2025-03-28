"""
Program Name: ICMPPingerfinal.py
Description: This program implements a simple ICMP-based ping utility that sends ICMP Echo Request
             packets to a specified host and waits for ICMP Echo Reply packets. It calculates and
             displays the Round Trip Time (RTT) for each packet and provides statistics such as
             packet loss, minimum, maximum, and average RTT.

Author: Ryan Ellis
Date: 3/27/2025

Course: COSC 370 - Computer Networks
Instructor: Dr. Enyue Lu

Usage:
    1. Run this program to send ICMP Echo Request packets to a specified host.
    2. The program will display the RTT for each packet and a summary of statistics at the end.

Requirements:
    - Python 3.x
    - Administrative/root privileges to create raw sockets.
    - The `socket`, `os`, `struct`, `time`, `select`, and `sys` libraries for ICMP communication.

Notes:
    - The program uses raw sockets, which require administrative/root privileges to run.
    - The host to ping can be modified in the `hostPing` variable in the `__main__` block.
    - This program is for educational purposes and is not intended for production use.
"""

import socket
import os
import struct
import time
import select
import sys          #import necessary libraries

# ICMP Constants
ICMP_ECHO_REQUEST = 8   # Type for ICMP Echo Request
ICMP_ECHO_REPLY = 0     # Type for ICMP Echo Reply
ICMP_HEADER_SIZE = 8    # Header size for ICMP

# Create checksum function for ICMP packet
def checksum(data):
    total = 0
    # Sum the 16-bit values of the packet
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + (data[i + 1])     # Shift and add each 16-bit block
        total = (total & 0xFFFF) + (total >> 16)
    # Return the complement of the checksum
    return ~total & 0xFFFF

# Create ICMP Echo Request packet with timestamp and return the packet
def createPacket(id, seq):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, seq)  # Create header with type, code, checksum, ID, sequence
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    payload = struct.pack("d", timestamp)  # Pack the timestamp as a double (8 bytes)
    checksumValue = checksum(header + payload)  # Calculate checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(checksumValue), id, seq)  # Rebuild header with checksum
    packet = header + payload  # Return the complete packet
    print(f"Created packet with ID {id} and sequence {seq}: {packet}")  # Output the packet
    return packet

# Receive the ICMP Echo Reply and calculate the RTT
def receivePing(icmpSocket, id, seq, timeout):
    startTime = time.time() # Record the start time
    while True:                     # Loop until a response is received or timeout
        ready = select.select([icmpSocket], [], [], timeout)    # read from the socket
        # Check if the socket is ready to read
        if ready[0] == []:
            return None  # Timeout if no response
        packet, addr = icmpSocket.recvfrom(1024)    # Receive the response
        print(f"Received raw packet: {packet}")
        icmpHeader = packet[20:28]  # Extract ICMP header from the response
        type, code, checksum, pid, seqReceived = struct.unpack("bbHHh", icmpHeader) # Unpack the header
        print(f"Received packet: type={type}, code={code}, checksum={checksum}, pid={pid}, seq={seqReceived}")
        if type == ICMP_ECHO_REPLY and pid == id and seqReceived == seq:    # Check if the packet is an Echo Reply and matches the ID and sequence
            endTime = time.time()   # Record the end time
            rtt = (endTime - startTime) * 1000  # RTT in milliseconds
            return rtt
    return None     # Return None if no response is received

# Main Ping function
def ping(host, timeout=1, count=10):
    # Create a raw socket for ICMP
    try:    #try to create a raw socket
        icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        print("Socket created successfully.")
    except PermissionError:
        print("Permission denied: You need to run this as root or with administrative privileges.")     # Check for permission error
        sys.exit(1)
    except Exception as e:
        print(f"Failed to create socket: {e}")      # Check for other socket creation errors
        sys.exit(1)

    try:    #try to resolve the host
        destIp = socket.gethostbyname(host)
        print(f"Resolved {host} to {destIp}")
    except socket.gaierror:
        print(f"Could not resolve host: {host}")
        sys.exit(1)

    print(f"Pinging {host} ({destIp}) with ICMP Echo Request:")

    rtts = []           # List to store RTTs
    lostPackets = 0     # Counter for lost packets
    minRtt, maxRtt, totalRtt = float('inf'), 0, 0       # Initialize min, max, and total RTT

    for i in range(count):
        time.sleep(1)
        packetId = (os.getpid() & 0xFFFF) + i  # Ensure packet ID is unique for each packet
        packet = createPacket(packetId, i + 1)
        try:
            icmpSocket.sendto(packet, (destIp, 1))  # Send the packet
            print(f"Sent packet with ID {packetId} and sequence {i + 1}")
        except Exception as e:
            print(f"Failed to send packet: {e}")        # Check for send errors
            lostPackets += 1
            continue

        rtt = receivePing(icmpSocket, packetId, i + 1, timeout)     # Wait for a response

        if rtt is None:     # If no response, increment lost packets
            lostPackets += 1
            print(f"Request {i+1}: Timeout")
        else:       # If response received, update RTT statistics
            rtts.append(rtt)
            totalRtt += rtt
            minRtt = min(minRtt, rtt)
            maxRtt = max(maxRtt, rtt)
            print(f"Request {i+1}: RTT = {rtt:.2f} ms")

    # Calculate packet loss
    packet_loss = (lostPackets / count) * 100

    # Print statistics
    if rtts:
        avg_rtt = totalRtt / len(rtts)
        print(f"\n--- {host} ping statistics ---")
        print(f"{count} packets transmitted, {count - lostPackets} received, {packet_loss:.2f}% packet loss")
        print(f"Total RTT = {totalRtt:.2f} ms")
        print(f"Average RTT = {avg_rtt:.2f} ms")
        print(f"Minimum RTT = {minRtt:.2f} ms")
        print(f"Maximum RTT = {maxRtt:.2f} ms")
    else:       # If no RTTs were recorded, all packets were lost
        print("All packets were lost")

    icmpSocket.close()  # Close the socket

if __name__ == "__main__":  # Main program

    hostPing = "127.0.0.1"  # Set hostPing to the desired host
    ping(hostPing)          #ping the host