import socket
import pyautogui
# TODO: look into a python library called `pyautogui` for controlling the keyboard from code.
# ask Nick for guidance if you would like!

localIP     = ''
localPort   = 20001
bufferSize  = 1024


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    # address = bytesAddressPair[1] # we don't care about the IP address the message came from
    print(f"Message from Client: '{message}'")
    
    # message will be a list of (capital) characters that were detected
    # so try something like:
    if "W" in message:
        pyautogui.keyDown('W')
    if "R" in message:
        pyautogui.keyDown('Q')
        pass # do something for "F"
    if "E" in message:
        pyautogui.keyDown('E')
        pass # do something for "F"
    if "C" in message:
        pyautogui.keyDown('C')
        pass # do something for "F"
    if "U" in message:
        pyautogui.keyDown('U')
        pass # do something for "F"
    if "H" in message:
        pyautogui.keyDown('H')
        pass # do something for "F"
    if message == "movef" :
        print("move!")