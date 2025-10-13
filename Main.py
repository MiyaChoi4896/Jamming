import time
import math
import random
import tkinter as tk
from tkinter import ttk, messagebox

# --- Device and Network Classes ---
class Device:
    def __init__(self, name, network):
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


    #Frequency type has been changed to only 2, update that in the code

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
    def __init__(self, root): #generic setyup stuff
        self.root = root
        self.root.title("Network Jamming Simulator Setup")
        self.device_entries = []
        self.data_rate = tk.StringVar(value="100") 
        self.jammer_power = tk.StringVar(value="1")
        self.jammer_gain = tk.StringVar(value="1") 
        self.setup_main_window()

    def setup_main_window(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack()

        #create buttons and text boxes here
        
        # Network type
        ttk.Label(frame, text="Select Frequency type:").grid(row=0, column=0, sticky="w")
        self.network_type = tk.StringVar(value="1")
        ttk.Radiobutton(frame, text="2.4", variable=self.network_type, value="1").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frame, text="5 GhZ", variable=self.network_type, value="2").grid(row=0, column=2, sticky="w")
        #ttk.Radiobutton(frame, text="5 wavelengths", variable=self.network_type, value="3").grid(row=0, column=3, sticky="w")

        #create devices based on user input
        ttk.Label(frame, text="Number of devices:").grid(row=1, column=0, sticky="w")
        self.num_devices = tk.IntVar(value=2)
        num_spin = ttk.Spinbox(frame, from_=2, to=8, textvariable=self.num_devices, width=5, command=self.update_device_entries)
        num_spin.grid(row=1, column=1, sticky="w")

        #user selects if a device will jam the network
        self.jamming_enabled = tk.BooleanVar()
        jamming_check = ttk.Checkbutton(frame, text="Enable Jamming", variable=self.jamming_enabled, command=self.toggle_jamming_type)
        jamming_check.grid(row=2, column=0, sticky="w")

        #on one row
        #user inputs jammer power in watts
        ttk.Label(frame, text="Jammer power (W)").grid(row=3, column=0, sticky="w")
        self.jammer_power = tk.IntVar(value=10)
        jammer_power_entry = ttk.Entry(frame, textvariable=self.jammer_power, width=5 )
        jammer_power_entry.grid(row=3, column=1, sticky="w", pady=(10,0))
        #jammer antenna gain in dB 
        ttk.Label(frame, text="Jammer Gain (dB)").grid(row=3, column=2, sticky="w")
        self.jammer_gain = tk.IntVar(value=10)
        jammer_gain_entry = ttk.Entry(frame, textvariable=self.jammer_gain, width=5 )
        jammer_gain_entry.grid(row=3, column=3, sticky="w", pady=(10,0))
        #R is calculated just of distance from the line (closest)



        #user inputs Data Rate
        ttk.Label(frame, text="Data Rate kb/s").grid(row=4, column=0, sticky="w")
        data_rate_entry = ttk.Entry(frame, textvariable=self.data_rate, width=5 )
        data_rate_entry.grid(row=4, column=1, sticky="w", pady=(10,0))
        #data rate reduces based on intercestion

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
        self.device_frame.grid(row=5, column=0, columnspan=4, sticky="w", pady=(10,0))
        self.update_device_entries()

        # Jammer radius slider NEED TO REMOVE THIS
        #ttk.Label(frame, text="Jammer Intensity").grid(row=6, column=0, sticky="w")
        #self.jammer_radius = tk.IntVar(value=100)
        #self.radius_slider = ttk.Scale(frame, from_=30, to=300, orient="horizontal", variable=self.jammer_radius)
        #self.radius_slider.grid(row=6, column=1, columnspan=2, sticky="we")
        #self.radius_value_label = ttk.Label(frame, textvariable=self.jammer_radius)
        #self.radius_value_label.grid(row=6, column=3, sticky="w")

        #Beam width
        ttk.Label(frame, text="Antenna Beamwidth").grid(row=7, column=0, sticky="w")
        self.beam_width = tk.IntVar(value=90)
        self.radius_slider = ttk.Scale(frame, from_=0, to=360, orient="horizontal", variable=self.beam_width)
        self.radius_slider.grid(row=7, column=1, columnspan=2, sticky="we")
        self.radius_value_label = ttk.Label(frame, textvariable=self.beam_width)
        self.radius_value_label.grid(row=7, column=3, sticky="w")

        # Submit button
        submit_btn = ttk.Button(frame, text="Submit", command=self.submit)
        submit_btn.grid(row=8, column=0, columnspan=4, pady=10)


    #get the jamming type or if its enabled/disabled
    def toggle_jamming_type(self):
        state = "!disabled" if self.jamming_enabled.get() else "disabled"
        for radio in self.jamming_type_radios:
            radio.state([state])

    #update the number of devices from user input and allow it to be named
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
            data_rate_val = float(self.data_rate.get())
            jammer_power_val = float(self.jammer_power.get())
            jammer_gain_val = float(self.jammer_gain.get())
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return
        jam_enabled = self.jamming_enabled.get()
        jam_type = self.jamming_type.get() if jam_enabled else None
        jammer_radius = (jammer_power_val * jammer_gain_val * 10 * math.sqrt(0.125)) / math.sqrt(4 * math.pi)
        #convert it from log to linear
        print(jammer_radius)
        self.data_rate_val = data_rate_val
        self.jammer_power_val = jammer_power_val
        self.jammer_gain_val = jammer_gain_val
        self.open_sim_window(ntype, ndev, names, jam_enabled, jam_type, jammer_radius)

    #make the sim window
    def open_sim_window(self, ntype, ndev, names, jam_enabled, jam_type, jammer_radius):
        sim = tk.Toplevel(self.root)
        sim.title("Network Simulation")
        canvas = tk.Canvas(sim, bg="#f0f0f0", width=680, height=460)
        canvas.pack(padx=10, pady=10)

        # Place devices and jammer
        self.device_objs = []  # Store (group, label) for each device
        self.device_positions = []  # Store (x, y) for each device
        positions = [(100 + i*100, 200) for i in range(ndev)]
        for i, (name, pos) in enumerate(zip(names, positions)):
            group = self.create_draggable(canvas, pos[0], pos[1], name, fill="#4a90e2", update_callback=self.update_lines)
            self.device_objs.append((group, name))
            self.device_positions.append([pos[0], pos[1]])
        # Add fake jammer (not connected by lines)
        # Draw jammer with radius
        if jam_enabled:
            self.jammer_obj = self.create_draggable(canvas, 350, 400, "Jammer", fill="#e24a4a", update_callback=self.update_jammer_radius)
            self.jammer_radius_val = jammer_radius
            self.jammer_radius_circle = self.draw_jammer_radius(canvas, 350, 400, self.beam_width.get(), self.jammer_radius_val)
            #self.arc_lines = self.draw_arc_lines(canvas, *self.get_jammer_center(), self.beam_width.get(), self.jammer_radius_val)
            self.sim_canvas = canvas

        # Draw lines between devices (fully connected)
        self.canvas = canvas
        self.device_lines = []
        self.draw_lines_between_devices()
        #self.draw_arc_lines()

    def draw_jammer_radius(self, canvas, x, y, arcAngle, radius):
        # Draw an arc representing the jammer's beam
        start_angle = -arcAngle/2
        extent_angle = arcAngle
        # create_arc
        return canvas.create_arc(x-radius, y-radius, x+radius, y+radius, start=90+start_angle, extent=extent_angle,outline="#e24a4a", width=2, style=tk.ARC)


    def get_jammer_center(self):
        # Get the center of the jammer oval
        oval = self.jammer_obj[0]
        coords = self.sim_canvas.coords(oval)
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        return x, y

    def update_jammer_radius(self):
        # Move the arc with the jammer and update its angle
        x, y = self.get_jammer_center()
        r = self.jammer_radius_val
        arcAngle = self.beam_width.get()
        self.sim_canvas.coords(self.jammer_radius_circle, x-r, y-r, x+r, y+r)
        self.sim_canvas.itemconfig(self.jammer_radius_circle, start=90-arcAngle/2, extent=arcAngle)
        self.update_lines()
        self.update_arc_lines()


    def draw_lines_between_devices(self):
        # Remove old lines and percentage labels
        for _, _, line_id, label_id in getattr(self, 'device_lines', []):
            self.canvas.delete(line_id)
            self.canvas.delete(label_id)
        self.device_lines = []
        n = len(self.device_objs)
        # Draw lines and percentage labels between every pair (i < j)
        for i in range(n):
            x1, y1 = self.get_device_center(i)
            for j in range(i+1, n):
                x2, y2 = self.get_device_center(j)
                line_id = self.canvas.create_line(x1, y1, x2, y2, fill="#888", width=2, tags="devline")
                # Calculate midpoint for label
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                label_id = self.canvas.create_text(mx, my, text=self.data_rate_val, font=("Arial", 10, "bold"), tags="percentlabel")
                # Intersection check
                if self.intersection_check(x1, y1, x2, y2, *self.get_jammer_center(), self.jammer_radius_val, self.beam_width.get()):
                    print("touching")
                #xj, yj = self.get_jammer_center()
                #rj = self.jammer_radius.get() if hasattr(self, 'jammer_radius') else getattr(self, 'jammer_radius_val', 100)
                #dx, dy = x2 - x1, y2 - y1
                #fx, fy = x1 - xj, y1 - yj
                #a = dx*dx + dy*dy
                #b = 2 * (fx*dx + fy*dy)
                #c = fx*fx + fy*fy - rj*rj
                #discriminant = b*b - 4*a*c
                #if discriminant >= 0 and a != 0:
                #    sqrt_disc = math.sqrt(discriminant)
                #    t1 = (-b - sqrt_disc) / (2*a)
                #    t2 = (-b + sqrt_disc) / (2*a)
                #    t_candidates = [t for t in [t1, t2] if 0 <= t <= 1]
                #    if t_candidates:
                #        print("touching")
                self.device_lines.append((i, j, line_id, label_id))
        # Ensure lines and labels are behind device ovals
        self.canvas.tag_lower("devline")
        self.canvas.tag_lower("percentlabel")

    def draw_arc_lines(self, canvas, x, y, arcAngle, radius):
        # Draw lines from the ends of the arc to the jammer
        start_angle = -arcAngle/2
        end_angle = arcAngle/2

        x1 = x + radius * math.sin(math.radians(start_angle))
        y1 = y - radius * math.cos(math.radians(start_angle))
        x2 = x + radius * math.sin(math.radians(end_angle))
        y2 = y - radius * math.cos(math.radians(end_angle))

        line1 = canvas.create_line(x, y, x1, y1, fill="#e24a4a", width=2)
        line2 = canvas.create_line(x, y, x2, y2, fill="#e24a4a", width=2)
        self.canvas.tag_lower(line1)
        self.canvas.tag_lower(line2)
        return line1, line2

    def update_arc_lines(self):
        # Redraw lines from the ends of the arc to the jammer
        if hasattr(self, 'arc_lines'):
            for line in self.arc_lines:
                self.sim_canvas.delete(line)
        x, y = self.get_jammer_center()
        arcAngle = self.beam_width.get()
        radius = self.jammer_radius_val
        self.arc_lines = self.draw_arc_lines(self.sim_canvas, x, y, arcAngle, radius)

    def get_device_center(self, idx):
        # Get the center of the oval for device idx
        group, _ = self.device_objs[idx]
        oval = group[0]
        coords = self.canvas.coords(oval)
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2
        return x, y

    def update_lines(self):
        # Redraw all device lines and move percentage labels
        for i, j, line_id, label_id in self.device_lines:
            x1, y1 = self.get_device_center(i)
            x2, y2 = self.get_device_center(j)
            self.canvas.coords(line_id, x1, y1, x2, y2)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.coords(label_id, mx, my)
            
            # Intersection check
            print(self.intersection_check(x1, y1, x2, y2, *self.get_jammer_center(), self.jammer_radius_val, self.beam_width.get()))


            #xj, yj = self.get_jammer_center()
            #rj = self.jammer_radius.get() if hasattr(self, 'jammer_radius') else getattr(self, 'jammer_radius_val', 100)
            #dx, dy = x2 - x1, y2 - y1
            #fx, fy = x1 - xj, y1 - yj
            #a = dx*dx + dy*dy
            #b = 2 * (fx*dx + fy*dy)
            #c = fx*fx + fy*fy - rj*rj
            #discriminant = b*b - 4*a*c
            #if discriminant >= 0 and a != 0:
            #    sqrt_disc = math.sqrt(discriminant)
            #    t1 = (-b - sqrt_disc) / (2*a)
            #    t2 = (-b + sqrt_disc) / (2*a)
            #    t_candidates = [t for t in [t1, t2] if 0 <= t <= 1]
            #    if t_candidates:
            #        print("touching")
            
        # Keep lines and labels behind devices after dragging
        self.canvas.tag_lower("devline")
        self.canvas.tag_lower("percentlabel")

    def intersection_check(self, x1, y1, x2, y2, xj, yj, rj, arc_angle):
        # Check if line (x1,y1)-(x2,y2) intersects the arc and return a percentage of the line inside the arc as a decimal
        dx, dy = x2 - x1, y2 - y1
        fx, fy = x1 - xj, y1 - yj
        a = dx*dx + dy*dy
        b = 2 * (fx*dx + fy*dy)
        c = fx*fx + fy*fy - rj*rj
        discriminant = b*b - 4*a*c
        points = []
        # Endpoints
        endpoints = [(x1, y1), (x2, y2)]
        # Helper: is a point inside the arc sector?
        def angle_in_arc(px, py):
            angle = math.degrees(math.atan2(py - yj, px - xj))
            angle = (angle + 360) % 360
            start_angle = (270 - arc_angle/2) % 360
            end_angle = (270 + arc_angle/2) % 360
            if start_angle < end_angle:
                return start_angle <= angle <= end_angle
            else:
                return angle >= start_angle or angle <= end_angle
        # Find intersection points with the circle
        if discriminant >= 0 and a != 0:
            sqrt_disc = math.sqrt(discriminant)
            t1 = (-b - sqrt_disc) / (2*a)
            t2 = (-b + sqrt_disc) / (2*a)
            for t in [t1, t2]:
                if 0 <= t <= 1:
                    px = x1 + t*dx
                    py = y1 + t*dy
                    points.append((px, py))
        # Collect all relevant points: endpoints inside the circle & arc, and intersection points inside arc
        relevant_points = []
        for px, py in endpoints + points:
            dist = math.hypot(px - xj, py - yj)
            if dist <= rj and angle_in_arc(px, py):
                relevant_points.append((px, py))
        # If no relevant points, check if the whole line is inside the arc sector and circle
        if not relevant_points:
            # Check midpoint
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            dist_mid = math.hypot(mx - xj, my - yj)
            if dist_mid <= rj and angle_in_arc(mx, my):
                return 1.0
            return 0.0
        # Sort points along the line
        relevant_points.sort(key=lambda p: math.hypot(p[0]-x1, p[1]-y1))
        # If only one relevant point, check which endpoint is inside
        if len(relevant_points) == 1:
            # Find closest endpoint inside arc & circle
            for px, py in endpoints:
                dist = math.hypot(px - xj, py - yj)
                if dist <= rj and angle_in_arc(px, py):
                    seg_len = math.hypot(px - relevant_points[0][0], py - relevant_points[0][1])
                    total_len = math.hypot(dx, dy)
                    return seg_len / total_len if total_len != 0 else 0.0
            return 0.0
        # If two or more relevant points, sum up the segments inside
        total_inside = 0.0
        for i in range(0, len(relevant_points)-1, 2):
            seg_len = math.hypot(relevant_points[i+1][0] - relevant_points[i][0],
                             relevant_points[i+1][1] - relevant_points[i][1])
            total_inside += seg_len
        total_len = math.hypot(dx, dy)
        return total_inside / total_len if total_len != 0 else 0.0
        

    def create_draggable(self, canvas, x, y, label, fill="#4a90e2", update_callback=None):
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
            if update_callback:
                update_callback()
        for item in group:
            canvas.tag_bind(item, '<ButtonPress-1>', on_press)
            canvas.tag_bind(item, '<B1-Motion>', on_drag)
        return group


# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk() #make main window, tell the code to use tk
    app = App(root) #also make main window
    root.mainloop()