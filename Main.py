class Device:
    def __init__(self, name):
        self.name = name
        
    def send(self, message, recipient):
        print(f"Sending message: {message} from {self.name} to {recipient.name}")
        recipient.receive(message, self)

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


#to do: user selects network type and no. of devices

#user selects if a device will jam the network



#create devices
DeviceA = Device("DeviceA")
DeviceB = Device("DeviceB")

#have a user input a message to send to DeviceB
userMessage = input("Enter a message to send to DeviceB: ")
DeviceA.send(userMessage, DeviceB)


#split the message the user sends into packets and send each packet separately

#that way jamming affects the individual packets

#have a loading bar of each packet being sent and recieved
#%of packets sent and recieved out of total 
 
userMessage = input("Enter a message to send to DeviceA: ")
DeviceB.send(userMessage, DeviceA)
    