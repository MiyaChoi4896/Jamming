import time
import random
import tkinter as tk
from tkinter import ttk, messagebox

# --- Device and Network Classes ---
class Device:
    def __init__(self, name, network=None):
        self.name = name
        self.network = network

    def send(self, message, recipient):
        if self.network:
            self.network.transmit(message, self, recipient)

    def receive(self, message, sender):
        print(f"{self.name} Received message: {message} from {sender.name}")
        

class Network:
    def __init__(self, network_type, jamming_enabled=False, jamming_type=None):
        self.network_type = network_type
        self.devices = []
        self.connections = set()
        self.jamming_enabled = jamming_enabled
        self.jamming_type = jamming_type

    def add_device(self, device):
        device.network = self
        self.devices.append(device)
        print(f"Device {device.name} added to {self.network_type} network.")
        # Initiate SYN/ACK handshake with all existing devices
        for other in self.devices:
            if other is not device:
                conn = tuple(sorted([device.name, other.name]))
                if conn not in self.connections:
                    print(f"{device.name} -> {other.name}: SYN")
                    print(f"{other.name} -> {device.name}: SYN-ACK")
                    print(f"{device.name} -> {other.name}: ACK")
                    self.connections.add(conn)

    def transmit(self, message, sender, recipient):
        print(f"Transmitting message: {message} from {sender.name} to {recipient.name} over {self.network_type} network.")
        #break message into packets and send each packet
        #each letter should be sent as a packet
        messagePacket = list(message)
        recievedPacketList = []
        freqSentOn = random.randint(1, self.network_type)
        for char in messagePacket:
            recievedPacketList.append(self.send_packet(char, freqSentOn))

        print(".")
        time.sleep(0.5)
        print("..")
        time.sleep(0.5)
        print("...")
        time.sleep(0.5)
        recipient.receive(''.join(recievedPacketList), sender)

    def send_packet(self, char, freqSentOn):
        #if spot is selected and jamming is enabled it jams the selected frequency
        #if the message gets transmitted on the jammed frequency it gets replaced with a "."
        #else nothing happens to the message
        if self.jamming_enabled and self.jamming_type == "1":
            if freqSentOn == 1:
                return "."
            else:
                return char
            

        
        #if 2: sweep is selected
        #the jammer sweeps through all frequencies randomly, jamming as it goes
        #each letter is sent through as a packet on a random frequency 
        if self.jamming_enabled and self.jamming_type == "2":
            if self.network_type == 1:
                #100% chance of jamming
                return "."
            elif self.network_type == 2:
                if random.random() < 0.33:
                    #33% chance of jamming
                    return "."
                else:
                    return char
            elif self.network_type == 3:
                #20% chance of jamming
                if random.random() < 0.2:
                    return "."
                else:
                    return char
                


        # Barrage jamming
        #all frequencies are jammed at once
        if self.jamming_enabled and self.jamming_type == "3":
            print("Session Disrupted")
            return "."
        return char

# --- GUI :sob: ---
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Jamming Simulator Setup")
        self.device_entries = []
        self.setup_main_window()

    def setup_main_window(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        # Network type
        ttk.Label(frame, text="Select network type:").grid(row=0, column=0, sticky="w")
        self.network_type = tk.StringVar(value="1")
        ttk.Radiobutton(frame, text="1 wavelength", variable=self.network_type, value="1").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frame, text="3 wavelengths", variable=self.network_type, value="2").grid(row=0, column=2, sticky="w")
        ttk.Radiobutton(frame, text="5 wavelengths", variable=self.network_type, value="3").grid(row=0, column=3, sticky="w")

        #create devices based on user input
        ttk.Label(frame, text="Number of devices:").grid(row=1, column=0, sticky="w")
        self.num_devices = tk.IntVar(value=2)
        num_spin = ttk.Spinbox(frame, from_=2, to=8, textvariable=self.num_devices, width=5, command=self.update_device_entries)
        num_spin.grid(row=1, column=1, sticky="w")

        #user selects if a device will jam the network
        self.jamming_enabled = tk.BooleanVar()
        jamming_check = ttk.Checkbutton(frame, text="Enable Jamming", variable=self.jamming_enabled, command=self.toggle_jamming_type)
        jamming_check.grid(row=2, column=0, sticky="w")

        # Jamming type
        self.jamming_type = tk.StringVar(value="1")
        self.jamming_type_frame = ttk.Frame(frame)
        self.jamming_type_frame.grid(row=2, column=1, columnspan=3, sticky="w")
        self.jamming_type_radios = [
            ttk.Radiobutton(self.jamming_type_frame, text="Spot", variable=self.jamming_type, value="1"),
            ttk.Radiobutton(self.jamming_type_frame, text="Sweep", variable=self.jamming_type, value="2"),
            ttk.Radiobutton(self.jamming_type_frame, text="Barrage", variable=self.jamming_type, value="3")
        ]
        for i, radio in enumerate(self.jamming_type_radios):
            radio.grid(row=0, column=i, sticky="w")
        self.toggle_jamming_type()

        # Device name entries
        self.device_frame = ttk.Frame(frame)
        self.device_frame.grid(row=3, column=0, columnspan=4, sticky="w", pady=(10,0))
        self.update_device_entries()

        # Submit button
        submit_btn = ttk.Button(frame, text="Submit", command=self.submit)
        submit_btn.grid(row=4, column=0, columnspan=4, pady=10)

    def toggle_jamming_type(self):
        state = "!disabled" if self.jamming_enabled.get() else "disabled"
        for radio in self.jamming_type_radios:
            radio.state([state])

    def update_device_entries(self):
        for widget in self.device_frame.winfo_children():
            widget.destroy()
        self.device_entries = []
        for i in range(self.num_devices.get()):
            ttk.Label(self.device_frame, text=f"Device {i+1} name:").grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.device_frame)
            entry.grid(row=i, column=1, sticky="w")
            entry.insert(0, f"Device{i+1}")
            self.device_entries.append(entry)

    def submit(self):
        # Gather all options
        try:
            ntype = int(self.network_type.get())
            ndev = int(self.num_devices.get())
            names = [e.get().strip() for e in self.device_entries]
            if len(set(names)) != ndev or any(not n for n in names):
                raise ValueError("Device names must be unique and non-empty.")
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return
        jam_enabled = self.jamming_enabled.get()
        jam_type = self.jamming_type.get() if jam_enabled else None
        self.open_sim_window(ntype, ndev, names, jam_enabled, jam_type)

    def open_sim_window(self, ntype, ndev, names, jam_enabled, jam_type):
        sim = tk.Toplevel(self.root)
        sim.title("Network Simulation")
        sim.geometry("700x500")
        canvas = tk.Canvas(sim, bg="#f0f0f0", width=680, height=460)
        canvas.pack(padx=10, pady=10)

        # Place devices and jammer
        objects = []
        positions = [(100 + i*100, 200) for i in range(ndev)]
        for i, (name, pos) in enumerate(zip(names, positions)):
            obj = self.create_draggable(canvas, pos[0], pos[1], name, fill="#4a90e2")
            objects.append(obj)
        # Add fake jammer
        jammer = self.create_draggable(canvas, 350, 400, "Jammer", fill="#e24a4a")
        objects.append(jammer)

        # Create network and devices for simulation logic
        self.sim_network = Network(ntype, jam_enabled, jam_type)
        self.sim_devices = [Device(name) for name in names]
        for dev in self.sim_devices:
            self.sim_network.add_device(dev)

    def create_draggable(self, canvas, x, y, label, fill="#4a90e2"):
        r = 30
        oval = canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline="#222", width=2)
        text = canvas.create_text(x, y, text=label, font=("Arial", 12, "bold"))
        group = [oval, text]
        def on_press(event, group=group):
            canvas._drag_data = (group, event.x, event.y)
        def on_drag(event, group=group):
            g, ox, oy = canvas._drag_data
            dx, dy = event.x - ox, event.y - oy
            for item in g:
                canvas.move(item, dx, dy)
            canvas._drag_data = (g, event.x, event.y)
        for item in group:
            canvas.tag_bind(item, '<ButtonPress-1>', on_press)
            canvas.tag_bind(item, '<B1-Motion>', on_drag)
        return group
    

    #fix devices sending messages to each other
    #add lines running inbetween devices to show connections
    #add a radius around the jammer to show its range
    #if the line intersects with the jammer radius it gets jammed if jamming is enabled


# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()