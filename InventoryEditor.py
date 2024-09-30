import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import struct

class BinEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Editor")

        self.filename = None

        # Create a Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Inventory tab
        self.inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_tab, text="Inventory")

        # Create Bugei tab
        self.bugei_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.bugei_tab, text="Bugei")

        # Create Kenpu tab
        self.kenpu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.kenpu_tab, text="Kenpu")

        # Create a canvas to hold the frames and scrollbar for the inventory
        self.canvas_inventory = tk.Canvas(self.inventory_tab)
        self.scrollbar_inventory = tk.Scrollbar(self.inventory_tab, orient="vertical", command=self.canvas_inventory.yview)
        self.scrollable_frame_inventory = tk.Frame(self.canvas_inventory)

        # Configure the scrollbar for inventory
        self.scrollable_frame_inventory.bind(
            "<Configure>",
            lambda e: self.canvas_inventory.configure(scrollregion=self.canvas_inventory.bbox("all"))
        )

        self.canvas_inventory.create_window((0, 0), window=self.scrollable_frame_inventory, anchor="nw")

        # Pack the canvas and scrollbar for the inventory
        self.canvas_inventory.configure(yscrollcommand=self.scrollbar_inventory.set)
        self.canvas_inventory.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_inventory.pack(side=tk.RIGHT, fill=tk.Y)

        # Load Button for Inventory
        self.load_button_inventory = tk.Button(self.inventory_tab, text="Load DATA.BIN", command=self.load_file)
        self.load_button_inventory.pack(pady=10)

        # Create frames for item entries in the inventory
        self.frames_inventory = []
        for i in range(30):
            frame = tk.Frame(self.scrollable_frame_inventory)
            frame.pack(pady=5)
            self.frames_inventory.append(frame)

            # Item ID
            label_id = tk.Label(frame, text=f"Item ID {i + 1}:")
            label_id.pack(side=tk.LEFT)
            entry_id = tk.Entry(frame, width=5)
            entry_id.pack(side=tk.LEFT)

            # Equipped (item)
            label_equipped = tk.Label(frame, text="Equipped:")
            label_equipped.pack(side=tk.LEFT)
            entry_equipped = tk.Entry(frame, width=5)
            entry_equipped.pack(side=tk.LEFT)

            # Amount
            label_amount = tk.Label(frame, text="Amount:")
            label_amount.pack(side=tk.LEFT)
            entry_amount = tk.Entry(frame, width=5)
            entry_amount.pack(side=tk.LEFT)

            # Equipped Type dropdown
            label_type = tk.Label(frame, text="Type:")
            label_type.pack(side=tk.LEFT)
            dropdown_type = ttk.Combobox(frame, values=["Unequipped (0)", "Sword (1)", "Accessory (2)"], width=15)
            dropdown_type.current(0)  # Default selection
            dropdown_type.pack(side=tk.LEFT)

            # Store references to entry widgets for later access
            setattr(self, f"item_id_{i}", entry_id)
            setattr(self, f"equipped_{i}", entry_equipped)
            setattr(self, f"amount_{i}", entry_amount)
            setattr(self, f"type_{i}", dropdown_type)

        # Save Button for Inventory
        self.save_button_inventory = tk.Button(self.inventory_tab, text="Save", command=self.save_file)
        self.save_button_inventory.pack(pady=10)

        # Create a canvas to hold the frames and scrollbar for the bugei
        self.canvas_bugei = tk.Canvas(self.bugei_tab)
        self.scrollbar_bugei = tk.Scrollbar(self.bugei_tab, orient="vertical", command=self.canvas_bugei.yview)
        self.scrollable_frame_bugei = tk.Frame(self.canvas_bugei)

        # Configure the scrollbar for bugei
        self.scrollable_frame_bugei.bind(
            "<Configure>",
            lambda e: self.canvas_bugei.configure(scrollregion=self.canvas_bugei.bbox("all"))
        )

        self.canvas_bugei.create_window((0, 0), window=self.scrollable_frame_bugei, anchor="nw")

        # Pack the canvas and scrollbar for the bugei
        self.canvas_bugei.configure(yscrollcommand=self.scrollbar_bugei.set)
        self.canvas_bugei.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_bugei.pack(side=tk.RIGHT, fill=tk.Y)

        # Create frames for Bugei entries
        self.frames_bugei = []
        for i in range(55):
            frame = tk.Frame(self.scrollable_frame_bugei)
            frame.pack(pady=5)
            self.frames_bugei.append(frame)

            # Length
            label_length = tk.Label(frame, text=f"Length {i + 1}:")
            label_length.pack(side=tk.LEFT)
            entry_length = tk.Entry(frame, width=5)
            entry_length.pack(side=tk.LEFT)

            # Bugei ID
            label_bugei_id = tk.Label(frame, text="Bugei ID:")
            label_bugei_id.pack(side=tk.LEFT)
            entry_bugei_id = tk.Entry(frame, width=5)
            entry_bugei_id.pack(side=tk.LEFT)

            # Kenpu ID slots
            for j in range(10):  # 10 Kenpu IDs per Bugei
                label_kenpu_id = tk.Label(frame, text=f"Kenpu ID {i + 1}.{j + 1}:")
                label_kenpu_id.pack(side=tk.LEFT)
                entry_kenpu_id = tk.Entry(frame, width=5)
                entry_kenpu_id.pack(side=tk.LEFT)

                # Store references to Kenpu ID entry widgets for later access
                setattr(self, f"kenpu_id_{i}_{j}", entry_kenpu_id)

            # Store references to entry widgets for later access
            setattr(self, f"length_{i}", entry_length)
            setattr(self, f"bugei_id_{i}", entry_bugei_id)

        # Save Button for Bugei
        self.save_button_bugei = tk.Button(self.bugei_tab, text="Save", command=self.save_bugei_file)
        self.save_button_bugei.pack(pady=10)

        # Create a canvas to hold the frames and scrollbar for the kenpu
        self.canvas_kenpu = tk.Canvas(self.kenpu_tab)
        self.scrollbar_kenpu = tk.Scrollbar(self.kenpu_tab, orient="vertical", command=self.canvas_kenpu.yview)
        self.scrollable_frame_kenpu = tk.Frame(self.canvas_kenpu)

        # Configure the scrollbar for kenpu
        self.scrollable_frame_kenpu.bind(
            "<Configure>",
            lambda e: self.canvas_kenpu.configure(scrollregion=self.canvas_kenpu.bbox("all"))
        )

        self.canvas_kenpu.create_window((0, 0), window=self.scrollable_frame_kenpu, anchor="nw")

        # Pack the canvas and scrollbar for the kenpu
        self.canvas_kenpu.configure(yscrollcommand=self.scrollbar_kenpu.set)
        self.canvas_kenpu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_kenpu.pack(side=tk.RIGHT, fill=tk.Y)

        # Create text boxes for Kenpu entries from 0x2C to 0xC6
        self.frames_kenpu = []
        for i in range(0x2C, 0xC7):
            frame = tk.Frame(self.scrollable_frame_kenpu)
            frame.pack(pady=5)
            self.frames_kenpu.append(frame)

            label_offset = tk.Label(frame, text=f"Offset {hex(i)[2:].upper()}:")
            label_offset.pack(side=tk.LEFT)
            entry_kenpu = tk.Entry(frame, width=5)
            entry_kenpu.pack(side=tk.LEFT)

            # Store references to Kenpu ID entry widgets for later access
            setattr(self, f"kenpu_entry_{i}", entry_kenpu)

        # Save Button for Kenpu
        self.save_button_kenpu = tk.Button(self.kenpu_tab, text="Save", command=self.save_kenpu_file)
        self.save_button_kenpu.pack(pady=10)

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if self.filename:
            try:
                with open(self.filename, "rb") as f:
                    # Load Inventory data
                    for i in range(30):
                        f.seek(0xD6 + i * 4)  # Adjusting the offset for each item
                        item_id_data = f.read(1)
                        equipped_data = f.read(1)
                        amount_data = f.read(1)
                        type_data = f.read(1)  # 1 byte for Equipped Type

                        item_id = item_id_data[0]
                        equipped = equipped_data[0]
                        amount = amount_data[0]
                        item_type = type_data[0]

                        # Populate the entries with hexadecimal values
                        getattr(self, f"item_id_{i}").delete(0, tk.END)
                        getattr(self, f"item_id_{i}").insert(0, hex(item_id)[2:].upper())  # Convert to hex

                        getattr(self, f"equipped_{i}").delete(0, tk.END)
                        getattr(self, f"equipped_{i}").insert(0, hex(equipped)[2:].upper())  # Convert to hex

                        getattr(self, f"amount_{i}").delete(0, tk.END)
                        getattr(self, f"amount_{i}").insert(0, hex(amount)[2:].upper())  # Convert to hex

                        # Set the type dropdown based on value
                        if item_type == 0:
                            getattr(self, f"type_{i}").current(0)  # Unequipped
                        elif item_type == 1:
                            getattr(self, f"type_{i}").current(1)  # Sword
                        else:
                            getattr(self, f"type_{i}").current(2)  # Accessory

                    # Load Bugei data
                    for i in range(55):
                        f.seek(0x2C8 + i * 0x0C)  # Adjusting the offset for each Bugei
                        length_data = f.read(1)
                        bugei_id_data = f.read(1)
                        kenpu_ids_data = f.read(10)  # 10 bytes for Kenpu IDs

                        length = length_data[0]
                        bugei_id = bugei_id_data[0]

                        # Populate the entries with hexadecimal values
                        getattr(self, f"length_{i}").delete(0, tk.END)
                        getattr(self, f"length_{i}").insert(0, hex(length)[2:].upper())  # Convert to hex

                        getattr(self, f"bugei_id_{i}").delete(0, tk.END)
                        getattr(self, f"bugei_id_{i}").insert(0, hex(bugei_id)[2:].upper())  # Convert to hex

                        for j in range(10):
                            kenpu_id = kenpu_ids_data[j]
                            getattr(self, f"kenpu_id_{i}_{j}").delete(0, tk.END)
                            getattr(self, f"kenpu_id_{i}_{j}").insert(0, hex(kenpu_id)[2:].upper())  # Convert to hex

                    # Load Kenpu data
                    for i in range(0x2C, 0xC7):
                        f.seek(i)  # Go to each offset from 0x2C to 0xC6
                        kenpu_data = f.read(1)

                        # Populate the entries with hexadecimal values
                        getattr(self, f"kenpu_entry_{i}").delete(0, tk.END)
                        getattr(self, f"kenpu_entry_{i}").insert(0, hex(kenpu_data[0])[2:].upper())  # Convert to hex

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.filename:
            try:
                with open(self.filename, "r+b") as f:
                    # Save Inventory data
                    for i in range(30):
                        f.seek(0xD6 + i * 4)  # Adjusting the offset for each item
                        new_item_id = int(getattr(self, f"item_id_{i}").get(), 16)  # Convert from hex
                        new_equipped = int(getattr(self, f"equipped_{i}").get(), 16)  # Convert from hex
                        new_amount = int(getattr(self, f"amount_{i}").get(), 16)  # Convert from hex
                        new_type = getattr(self, f"type_{i}").current()  # Get index of selected type

                        # Write the new values to the binary file
                        f.write(struct.pack("B", new_item_id))  # Write Item ID
                        f.write(struct.pack("B", new_equipped))  # Write Equipped
                        f.write(struct.pack("B", new_amount))  # Write Amount
                        f.write(struct.pack("B", new_type))  # Write Equipped Type as byte

                messagebox.showinfo("Success", "File saved successfully!")

            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid hexadecimal numbers.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_bugei_file(self):
        if self.filename:
            try:
                with open(self.filename, "r+b") as f:
                    # Save Bugei data
                    for i in range(55):
                        f.seek(0x2c8 + i * 0x0C)  # Adjusting the offset for each Bugei
                        new_length = int(getattr(self, f"length_{i}").get(), 16)  # Convert from hex
                        new_bugei_id = int(getattr(self, f"bugei_id_{i}").get(), 16)  # Convert from hex

                        # Write the new values to the binary file
                        f.write(struct.pack("B", new_length))  # Write Length as byte
                        f.write(struct.pack("B", new_bugei_id))  # Write Bugei ID as byte

                        for j in range(10):
                            new_kenpu_id = int(getattr(self, f"kenpu_id_{i}_{j}").get(), 16)  # Convert from hex
                            f.write(struct.pack("B", new_kenpu_id))  # Write Kenpu ID as byte

                messagebox.showinfo("Success", "Bugei data saved successfully!")

            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid hexadecimal numbers.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_kenpu_file(self):
        if self.filename:
            try:
                with open(self.filename, "r+b") as f:
                    # Save Kenpu data
                    for i in range(0x2C, 0xC7):
                        new_value = int(getattr(self, f"kenpu_entry_{i}").get(), 16)  # Convert from hex
                        f.seek(i)  # Go to the correct offset
                        f.write(struct.pack("B", new_value))  # Write byte

                messagebox.showinfo("Success", "Kenpu data saved successfully!")

            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid hexadecimal numbers.")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = BinEditor(root)
    root.mainloop()
