import time
import random
class Device:
    def __init__(self, name):
        self.name = name
        
    def send(self, message, recipient):
        #use the tansmit function of the network to send the message
        network.transmit(message, self, recipient)

    def receive(self, message, sender):
        print(f"{self.name} Received message: {message} from {sender.name}")

class Network:
    def __init__(self, network_type):
        self.network_type = network_type
        self.devices = []
        
    def add_device(self, device):
        self.devices.append(device)
        print(f"Device {device.name} added to {self.network_type} network.")
    
    def transmit(self, message, sender, recipient):
        print(f"Transmitting message: {message} from {sender.name} to {recipient.name} over {self.network_type} network.")
        print(".")
        time.sleep(0.5)
        print("..")
        time.sleep(0.5)
        print("...")
        time.sleep(0.5)
        recipient.receive(message, sender)
        


#to do: user selects network type and no. of device

validNetwork = False
while validNetwork == False:
    networkType = input("Select network type (1,2,3): ") #change later
    if networkType == "1":
        network = Network(1)
        validNetwork = True
    elif networkType == "2":
        network = Network(2)
        validNetwork = True
    elif networkType == "3":
        network = Network(3)
        validNetwork = True
    else:
        print("Invalid network type selected.")

noOfDevices = int(input("Enter number of devices (2 is recommended): "))

#user selects if a device will jam the network
userJamming = input("Enable jamming? (y/n): ")
if userJamming.lower() == 'y':
    jammingEnabled = True
else:
    jammingEnabled = False



#create devices based on user input

devices = []
for i in range(noOfDevices):
    deviceName = input(f"Enter name for Device {i+1}: ")
    newDevice = Device(deviceName)
    devices.append(newDevice)
    network.add_device(newDevice)

#Sending messages via devices
#loop through devices, n sends a message to n+1
#ask user to input each message
#if device is the last device, it sends to the first device
for i in range(noOfDevices):
    if i == noOfDevices - 1:
        sender = devices[i]
        recipient = devices[0]
    else:
        sender = devices[i]
        recipient = devices[i + 1]
    
    userMessage = input(f"Enter a message to send from {sender.name} to {recipient.name}: ")
    sender.send(userMessage, recipient)

#split the message the user sends into packets and send each packet separately

#that way jamming affects the individual packets

#have a loading bar of each packet being sent and recieved
#%of packets sent and recieved out of total 
 

    