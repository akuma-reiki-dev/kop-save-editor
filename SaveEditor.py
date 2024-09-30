import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import struct  # Import struct module for packing/unpacking binary data

class BinEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Kingdom Of Paradise Save Editor")

        self.filename = None

        # Create a Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # Create Main Tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        # Create other tabs

        self.chi_arts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chi_arts_tab, text="Chi Arts")

        # Main Tab Layout
        self.create_main_tab()
        
        # Chi Arts Tab Layout
        self.create_chi_arts_tab()

    def create_main_tab(self):
        # Load Button
        self.load_button = tk.Button(self.main_tab, text="Load DATA.BIN", command=self.load_file)
        self.load_button.pack(pady=10)

        # Frame for Save File Name Label and Entry
        name_frame = tk.Frame(self.main_tab)
        name_frame.pack(pady=5)

        # Label for Save File Name
        self.name_label = tk.Label(name_frame, text="Save File Name:")
        self.name_label.pack(side=tk.LEFT)

        # Text Box for editing Save File Name
        self.name_entry = tk.Entry(name_frame, width=30)  # Increased width for string
        self.name_entry.pack(side=tk.LEFT)

        # Frame for Taichi Label and Entry
        taichi_frame = tk.Frame(self.main_tab)
        taichi_frame.pack(pady=5)

        # Label for Taichi
        self.taichi_label = tk.Label(taichi_frame, text="Taichi:")
        self.taichi_label.pack(side=tk.LEFT)

        # Text Box for editing Taichi
        self.taichi_entry = tk.Entry(taichi_frame, validate="key", width=10)
        self.taichi_entry['validatecommand'] = (self.main_tab.register(self.validate_input), '%S')
        self.taichi_entry.pack(side=tk.LEFT)

        # Frame for Steel Orbs Label and Entry
        steel_frame = tk.Frame(self.main_tab)
        steel_frame.pack(pady=5)

        # Label for Steel Orbs
        self.steel_label = tk.Label(steel_frame, text="Steel Orbs:")
        self.steel_label.pack(side=tk.LEFT)

        # Text Box for editing Steel Orbs
        self.steel_entry = tk.Entry(steel_frame, validate="key", width=10)
        self.steel_entry['validatecommand'] = (self.main_tab.register(self.validate_input), '%S')
        self.steel_entry.pack(side=tk.LEFT)

        # Frame for Max HP Label and Entry
        max_hp_frame = tk.Frame(self.main_tab)
        max_hp_frame.pack(pady=5)

        # Label for Max HP
        self.max_hp_label = tk.Label(max_hp_frame, text="Max HP:")
        self.max_hp_label.pack(side=tk.LEFT)

        # Text Box for editing Max HP
        self.max_hp_entry = tk.Entry(max_hp_frame, validate="key", width=10)
        self.max_hp_entry['validatecommand'] = (self.main_tab.register(self.validate_input), '%S')
        self.max_hp_entry.pack(side=tk.LEFT)

        # Frame for Body Label and Entry
        body_frame = tk.Frame(self.main_tab)
        body_frame.pack(pady=5)

        # Label for Body
        self.body_label = tk.Label(body_frame, text="Body:")
        self.body_label.pack(side=tk.LEFT)

        # Text Box for editing Body
        self.body_entry = tk.Entry(body_frame, validate="key", width=10)
        self.body_entry['validatecommand'] = (self.main_tab.register(self.validate_body_technique_mind), '%S')
        self.body_entry.pack(side=tk.LEFT)

        # Frame for Technique Label and Entry
        technique_frame = tk.Frame(self.main_tab)
        technique_frame.pack(pady=5)

        # Label for Technique
        self.technique_label = tk.Label(technique_frame, text="Technique:")
        self.technique_label.pack(side=tk.LEFT)

        # Text Box for editing Technique
        self.technique_entry = tk.Entry(technique_frame, validate="key", width=10)
        self.technique_entry['validatecommand'] = (self.main_tab.register(self.validate_body_technique_mind), '%S')
        self.technique_entry.pack(side=tk.LEFT)

        # Frame for Mind Label and Entry
        mind_frame = tk.Frame(self.main_tab)
        mind_frame.pack(pady=5)

        # Label for Mind
        self.mind_label = tk.Label(mind_frame, text="Mind:")
        self.mind_label.pack(side=tk.LEFT)

        # Text Box for editing Mind
        self.mind_entry = tk.Entry(mind_frame, validate="key", width=10)
        self.mind_entry['validatecommand'] = (self.main_tab.register(self.validate_body_technique_mind), '%S')
        self.mind_entry.pack(side=tk.LEFT)

        # Frame for Level Label and Entry
        level_frame = tk.Frame(self.main_tab)
        level_frame.pack(pady=5)

        # Label for Level
        self.level_label = tk.Label(level_frame, text="Level:")
        self.level_label.pack(side=tk.LEFT)

        # Text Box for editing Level
        self.level_entry = tk.Entry(level_frame, validate="key", width=10)
        self.level_entry['validatecommand'] = (self.main_tab.register(self.validate_input), '%S')
        self.level_entry.pack(side=tk.LEFT)

        # Frame for Hiken Arts Checkbox
        hiken_frame = tk.Frame(self.main_tab)
        hiken_frame.pack(pady=5)

        # Checkbox for Hiken Arts
        self.hiken_var = tk.BooleanVar()
        self.hiken_checkbox = tk.Checkbutton(hiken_frame, text="Hiken Arts", variable=self.hiken_var)
        self.hiken_checkbox.pack(side=tk.LEFT)

        # Save Button
        self.save_button = tk.Button(self.main_tab, text="Save", command=self.save_file)
        self.save_button.pack(pady=10)

    def create_chi_arts_tab(self):
        # Selected Chi Art
        self.chi_art_label = tk.Label(self.chi_arts_tab, text="Selected Chi Art:")
        self.chi_art_label.pack(pady=5)

        # Dropdown for Selected Chi Art
        self.chi_art_var = tk.StringVar()
        self.chi_art_dropdown = ttk.Combobox(self.chi_arts_tab, textvariable=self.chi_art_var, state="readonly")
        self.chi_art_dropdown['values'] = ["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"]
        self.chi_art_dropdown.pack(pady=5)

        # Chi Art Levels Dropdowns
        self.chi_art_levels = {}
        for chi_art in ["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"]:
            frame = tk.Frame(self.chi_arts_tab)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"{chi_art} Levels:")
            label.pack(side=tk.LEFT)

            level_var = tk.StringVar()
            dropdown = ttk.Combobox(frame, textvariable=level_var, state="readonly")
            dropdown['values'] = [str(i) for i in range(4)]  # Options from 0 to 3
            dropdown.pack(side=tk.LEFT)
            self.chi_art_levels[chi_art] = level_var  # Store reference to the variable

        # Chi Art XP Textboxes
        self.chi_art_xp_entries = {}
        for chi_art in ["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"]:
            frame = tk.Frame(self.chi_arts_tab)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"{chi_art} XP:")
            label.pack(side=tk.LEFT)

            xp_entry_low = tk.Entry(frame, width=5)
            xp_entry_low.pack(side=tk.LEFT)
            xp_entry_high = tk.Entry(frame, width=5)
            xp_entry_high.pack(side=tk.LEFT)

            self.chi_art_xp_entries[chi_art] = (xp_entry_low, xp_entry_high)  # Store references to the entries

    def validate_input(self, new_value):
        if new_value == "" or (new_value.isdigit() and int(new_value) <= 9999):
            return True
        return False
    
    def validate_body_technique_mind(self, new_value):
        if new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 200):
            return True
        return False

    def load_file(self):
        self.filename = filedialog.askopenfilename(title="Select DATA.BIN File", filetypes=[("Binary Files", "*.bin")])
        if self.filename:
            try:
                with open(self.filename, "rb") as f:
                    # Load Save File Name value
                    f.seek(0x00)  # Seek to offset 0x00000000
                    name_bytes = f.read(30)  # Read 30 bytes for the name
                    self.name_entry.delete(0, tk.END)  # Clear previous value
                    self.name_entry.insert(0, name_bytes.decode("utf-16le").rstrip('\x00'))  # Insert new value

                    # Load Taichi value
                    f.seek(0x20)  # Seek to offset 0x00000020
                    taichi_value = struct.unpack("<h", f.read(2))[0]  # Unpack as little-endian signed short
                    self.taichi_entry.delete(0, tk.END)  # Clear previous value
                    self.taichi_entry.insert(0, str(taichi_value))  # Insert new value

                    # Load Steel Orbs value
                    f.seek(0x28)  # Seek to offset 0x00000028
                    steel_value = struct.unpack("<h", f.read(2))[0]  # Unpack as little-endian signed short
                    self.steel_entry.delete(0, tk.END)  # Clear previous value
                    self.steel_entry.insert(0, str(steel_value))  # Insert new value

                    # Load Max HP value
                    f.seek(0x220)  # Seek to offset 0x00000220
                    max_hp_value = struct.unpack("<h", f.read(2))[0]  # Unpack as little-endian signed short
                    self.max_hp_entry.delete(0, tk.END)  # Clear previous value
                    self.max_hp_entry.insert(0, str(max_hp_value))  # Insert new value

                    # Load Body value
                    f.seek(0x22A)  # Seek to offset 0x0000022A
                    body_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.body_entry.delete(0, tk.END)  # Clear previous value
                    self.body_entry.insert(0, str(body_value))  # Insert new value

                    # Load Technique value
                    f.seek(0x22C)  # Seek to offset 0x0000022C
                    technique_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.technique_entry.delete(0, tk.END)  # Clear previous value
                    self.technique_entry.insert(0, str(technique_value))  # Insert new value

                    # Load Mind value
                    f.seek(0x22E)  # Seek to offset 0x0000022E
                    mind_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.mind_entry.delete(0, tk.END)  # Clear previous value
                    self.mind_entry.insert(0, str(mind_value))  # Insert new value

                    # Load Level value
                    f.seek(0x230)  # Seek to offset 0x00000230
                    level_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.level_entry.delete(0, tk.END)  # Clear previous value
                    self.level_entry.insert(0, str(level_value))  # Insert new value

                    # Load Selected Chi Art value
                    f.seek(0x231)  # Seek to offset 0x00000231
                    chi_art_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.chi_art_var.set(["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"][chi_art_value])  # Set dropdown value

                    # Load Chi Art Levels
                    chi_art_levels_offsets = {
                        "Seiryu": 0x24E,
                        "Kirin": 0x24F,
                        "Genbu": 0x250,
                        "Suzaku": 0x251,
                        "Byakko": 0x252
                    }
                    for chi_art, offset in chi_art_levels_offsets.items():
                        f.seek(offset)  # Seek to offset for each Chi Art Level
                        level_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for level
                        self.chi_art_levels[chi_art].set(str(level_value))  # Set dropdown value

                    # Load Chi Art XP
                    chi_art_xp_offsets = {
                        "Seiryu": (0x232, 0x233),
                        "Kirin": (0x234, 0x235),
                        "Genbu": (0x236, 0x237),
                        "Suzaku": (0x238, 0x239),
                        "Byakko": (0x23A, 0x23B)
                    }
                    for chi_art, (low_offset, high_offset) in chi_art_xp_offsets.items():
                        f.seek(low_offset)  # Seek to low offset for XP
                        xp_low_value = struct.unpack("<B", f.read(1))[0]  # Read low XP value as 8-bit
                        self.chi_art_xp_entries[chi_art][0].delete(0, tk.END)  # Clear previous value
                        self.chi_art_xp_entries[chi_art][0].insert(0, str(xp_low_value))  # Insert new low XP value

                        f.seek(high_offset)  # Seek to high offset for XP
                        xp_high_value = struct.unpack("<B", f.read(1))[0]  # Read high XP value as 8-bit
                        self.chi_art_xp_entries[chi_art][1].delete(0, tk.END)  # Clear previous value
                        self.chi_art_xp_entries[chi_art][1].insert(0, str(xp_high_value))  # Insert new high XP value

                    # Load Hiken Arts value
                    f.seek(0x243)  # Seek to offset 0x00000243
                    hiken_value = struct.unpack("<B", f.read(1))[0]  # Read 1 byte for an 8-bit unsigned integer
                    self.hiken_var.set(hiken_value == 0x10)  # Set checkbox value (10 for on)

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.filename:
            try:
                new_name = self.name_entry.get().encode("utf-16le")[:30]  # Encode to UTF-16 LE and limit to 30 bytes
                taichi_value = int(self.taichi_entry.get())
                steel_value = int(self.steel_entry.get())
                max_hp_value = int(self.max_hp_entry.get())
                body_value = int(self.body_entry.get())
                technique_value = int(self.technique_entry.get())
                mind_value = int(self.mind_entry.get())
                level_value = int(self.level_entry.get())
                chi_art_index = ["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"].index(self.chi_art_var.get())
                hiken_value = 0x10 if self.hiken_var.get() else 0x00

                # Validate Chi Art Levels
                chi_art_levels_offsets = {
                    "Seiryu": 0x24E,
                    "Kirin": 0x24F,
                    "Genbu": 0x250,
                    "Suzaku": 0x251,
                    "Byakko": 0x252
                }
                chi_art_levels_values = {chi_art: int(level.get()) for chi_art, level in self.chi_art_levels.items()}

                # Validate XP values
                chi_art_xp_offsets = {
                    "Seiryu": (0x232, 0x233),
                    "Kirin": (0x234, 0x235),
                    "Genbu": (0x236, 0x237),
                    "Suzaku": (0x238, 0x239),
                    "Byakko": (0x23A, 0x23B)
                }
                chi_art_xp_values = {chi_art: (int(xp[0].get()), int(xp[1].get())) for chi_art, xp in self.chi_art_xp_entries.items()}

                # Validate all values
                if (-32768 <= taichi_value <= 32767 and
                    -32768 <= steel_value <= 32767 and
                    0 <= max_hp_value <= 65535 and
                    0 <= body_value <= 200 and
                    0 <= technique_value <= 200 and
                    0 <= mind_value <= 200 and
                    0 <= level_value <= 200 and
                    all(0 <= value <= 3 for value in chi_art_levels_values.values()) and  # Validate Chi Art Levels
                    all(0 <= xp[0] <= 65535 and 0 <= xp[1] <= 65535 for xp in chi_art_xp_values.values())):  # Validate XP values
                    with open(self.filename, "r+b") as f:
                        # Save Save File Name value
                        f.seek(0x00)  # Seek to offset 0x00000000
                        f.write(new_name.ljust(30, b'\x00'))  # Write name (30 bytes)

                        # Save Taichi value
                        f.seek(0x20)  # Seek to offset 0x00000020
                        f.write(struct.pack("<h", taichi_value))  # Write as little-endian signed short

                        # Save Steel Orbs value
                        f.seek(0x28)  # Seek to offset 0x00000028
                        f.write(struct.pack("<h", steel_value))  # Write as little-endian signed short

                        # Save Max HP value
                        f.seek(0x220)  # Seek to offset 0x00000220
                        f.write(struct.pack("<h", max_hp_value))  # Write as little-endian signed short

                        # Save Body value
                        f.seek(0x22A)  # Seek to offset 0x0000022A
                        f.write(struct.pack("<B", body_value))  # Write as an 8-bit unsigned integer

                        # Save Technique value
                        f.seek(0x22C)  # Seek to offset 0x0000022C
                        f.write(struct.pack("<B", technique_value))  # Write as an 8-bit unsigned integer

                        # Save Mind value
                        f.seek(0x22E)  # Seek to offset 0x0000022E
                        f.write(struct.pack("<B", mind_value))  # Write as an 8-bit unsigned integer

                        # Save Level value
                        f.seek(0x230)  # Seek to offset 0x00000230
                        f.write(struct.pack("<B", level_value))  # Write as an 8-bit unsigned integer

                        # Save Selected Chi Art value
                        f.seek(0x231)  # Seek to offset 0x00000231
                        f.write(struct.pack("<B", chi_art_index))  # Write as an 8-bit unsigned integer

                        # Save Chi Art Levels
                        for chi_art, offset in chi_art_levels_offsets.items():
                            f.seek(offset)  # Seek to offset for each Chi Art Level
                            f.write(struct.pack("<B", chi_art_levels_values[chi_art]))  # Write level

                        # Save Chi Art XP
                        for chi_art, (low_offset, high_offset) in chi_art_xp_offsets.items():
                            f.seek(low_offset)  # Seek to low offset for XP
                            f.write(struct.pack("<B", chi_art_xp_values[chi_art][0]))  # Write low XP value as 8-bit

                            f.seek(high_offset)  # Seek to high offset for XP
                            f.write(struct.pack("<B", chi_art_xp_values[chi_art][1]))  # Write high XP value as 8-bit

                        # Save Hiken Arts value
                        f.seek(0x243)  # Seek to offset 0x00000243
                        f.write(struct.pack("<B", hiken_value))  # Write as an 8-bit unsigned integer

                        messagebox.showinfo("Success", "Save file updated successfully.")
                else:
                    messagebox.showerror("Validation Error", "One or more values are out of range.")

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_widgets(self):
        # Create Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        # Create Chi Arts tab
        self.chi_arts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chi_arts_tab, text="Chi Arts")

        # Create Selected Chi Art Dropdown
        self.chi_art_var = tk.StringVar()
        self.chi_art_label = ttk.Label(self.chi_arts_tab, text="Selected Chi Art:")
        self.chi_art_label.grid(row=0, column=0, padx=10, pady=5)
        self.chi_art_dropdown = ttk.Combobox(self.chi_arts_tab, textvariable=self.chi_art_var,
                                              values=["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"])
        self.chi_art_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Create Chi Art Level Dropdowns
        self.chi_art_levels = {}
        for i, chi_art in enumerate(["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"], start=1):
            label = ttk.Label(self.chi_arts_tab, text=f"{chi_art} Chi Art Level:")
            label.grid(row=i, column=0, padx=10, pady=5)

            self.chi_art_levels[chi_art] = tk.StringVar(value="0")
            dropdown = ttk.Combobox(self.chi_arts_tab, textvariable=self.chi_art_levels[chi_art],
                                     values=["0", "1", "2", "3"])
            dropdown.grid(row=i, column=1, padx=10, pady=5)

        # Create Chi Art XP Textboxes
        self.chi_art_xp_entries = {}
        for i, chi_art in enumerate(["Seiryu", "Kirin", "Genbu", "Suzaku", "Byakko"], start=6):
            label = ttk.Label(self.chi_arts_tab, text=f"{chi_art} XP (Low):")
            label.grid(row=i, column=0, padx=10, pady=5)

            low_xp_entry = ttk.Entry(self.chi_arts_tab)
            low_xp_entry.grid(row=i, column=1, padx=10, pady=5)
            self.chi_art_xp_entries[chi_art] = (low_xp_entry,)

            label = ttk.Label(self.chi_arts_tab, text=f"{chi_art} XP (High):")
            label.grid(row=i, column=2, padx=10, pady=5)

            high_xp_entry = ttk.Entry(self.chi_arts_tab)
            high_xp_entry.grid(row=i, column=3, padx=10, pady=5)
            self.chi_art_xp_entries[chi_art] += (high_xp_entry,)

        # Load and Save buttons
        self.load_button = ttk.Button(self.chi_arts_tab, text="Load", command=self.load_file)
        self.load_button.grid(row=12, column=0, padx=10, pady=10)

        self.save_button = ttk.Button(self.chi_arts_tab, text="Save", command=self.save_file)
        self.save_button.grid(row=12, column=1, padx=10, pady=10)

        # Create other UI components as needed...

if __name__ == "__main__":
    root = tk.Tk()
    app = BinEditor(root)
    root.mainloop()
