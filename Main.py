class Device:
    def __init__(self, name):
        self.name = name
        
    def send(self, message, recipient):
        print(f"Sending message: {message} from {self.name} to {recipient.name}")
        recipient.receive(message, self)

    def receive(self, message, sender):
        print(f"{self.name} Received message: {message} from {sender.name}")


#create devices
DeviceA = Device("DeviceA")
DeviceB = Device("DeviceB")

#send and receive messages
DeviceA.send("Hello, DeviceB!", DeviceB)
DeviceB.send("Hello, DeviceA!", DeviceA)

    