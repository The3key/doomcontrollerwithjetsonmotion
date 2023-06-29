from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import socket
import sys

# Setup: Create a UDP socket at client side
serverAddressPort   = ("192.168.137.1", 20001)
# NOTE: This is the IP address ^ of the laptop on its hotspot.
# I found it by running this command in the Jetson terminal: `ip route`
# telling me the route from the Jetson to the wider internet.
# The first hop is the laptop hotspit, with this IP.
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Setup: Declare a helper function to simplify the "send message" call
def send_message(msg: str):
    UDPClientSocket.sendto(msg.encode(), serverAddressPort)

input_list = [ ]
letter_map = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"

net = detectNet("ssd-mobilenet-v2", threshold=0.5,
                # NOTE: These are the same command-line arguments to run our own model,
                # just copied into python-land
                model="models/asl_clean/ssd-mobilenet.onnx",
                labels="models/asl_clean/labels.txt",
                input_blob="input_0", output_cvg="scores", output_bbox="boxes")
camera = videoSource("/dev/video0")      # '/dev/video0' for V4L2
display = videoOutput("webrtc://@:8554/my_output") # 'my_video.mp4' for file

while True: 
   img = camera.Capture()

   if img is None: # capture timeout
      continue

   detections = net.Detect(img)

   # convert detections to a string of detected letters
   # ----
   # detected_letters_list = []
   # for detection in detections:
   #    detected_letters_list.append(letter_map[detection.ClassID])
   # detected_letters = ''.join(detected_letters_list)
   # ----
   # or more concisely:
   detected_letters = ''.join([letter_map[detection.ClassID] for detection in detections])
   # if any letters detected, print them and send them to the host computer
   if detected_letters:
      print(detected_letters)
      send_message(detected_letters)
      
   display.Render(img)
   display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

