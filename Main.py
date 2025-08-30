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
        #break message into packets and send each packet
        #each letter should be sent as a packet
        messagePacket = list(message)
        recievedPacketList = []
        for char in messagePacket:
            recievedPacketList.append(self.send_packet(char, sender, recipient))

        print(".")
        time.sleep(0.5)
        print("..")
        time.sleep(0.5)
        print("...")
        time.sleep(0.5)
        recipient.receive(''.join(recievedPacketList), sender)

    def send_packet(self, char, sender, recipient):
        if jammingEnabled and random.random() < 0.3:
            #replace the packet with a "."
            return "."  
        else:
            return char
        

#main
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


#have a loading bar of each packet being sent and recieved
#%of packets sent and recieved out of total 
 

    