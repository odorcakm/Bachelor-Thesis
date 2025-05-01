import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np

def calculate_transform(x1, y1, ra1, dec1, x2, y2, ra2, dec2, x3, y3, ra3, dec3):
    A_ra = np.array([[x1, y1, 1],
                     [x2, y2, 1],
                     [x3, y3, 1]])
    B_ra = np.array([ra1, ra2, ra3])
    a, b, c = np.linalg.solve(A_ra, B_ra)
    
    A_dec = np.array([[x1, y1, 1],
                      [x2, y2, 1],
                      [x3, y3, 1]])
    B_dec = np.array([dec1, dec2, dec3])
    d, e, f = np.linalg.solve(A_dec, B_dec)
    
    return a, b, c, d, e, f

def transform_coordinates(a, b, c, d, e, f, x, y):
    ra = a * x + b * y + c
    dec = d * x + e * y + f
    return ra, dec

def deg_to_sec(coord):
    coord_array = coord.split()
    seconds = float(coord_array[0]) * 3600 + float(coord_array[1]) * 60 + float(coord_array[2])
    return seconds

def sec_to_deg(sec):
    deg = int(sec // 3600)
    min = int((sec - deg * 3600) // 60)
    sec = sec - deg * 3600 - min * 60
    return f"{deg} {min} {sec}"

def center_of_coord(x):
    return x / 2

# GUI Functionality
class StarFieldCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Star Field Coordinate Calculator")

        # Headers
        tk.Label(root, text="Star Name").grid(row=0, column=0)
        tk.Label(root, text="x").grid(row=0, column=1)
        tk.Label(root, text="y").grid(row=0, column=2)
        tk.Label(root, text="RA").grid(row=0, column=3)
        tk.Label(root, text="Dec").grid(row=0, column=4)

        # Input fields for 3 stars
        self.entries = {}
        for i in range(1, 4):
            # Row for star name
            tk.Label(root, text=f"Star {i} Name:").grid(row=i*2-1, column=0, sticky='w')
            self.entries[f"name{i}"] = tk.Entry(root, width=15)
            self.entries[f"name{i}"].grid(row=i*2, column=0)

            # Row for coordinates
            tk.Label(root, text=f"Star {i} Coordinates:").grid(row=i*2-1, column=1, columnspan=4, sticky='w')
            self.entries[f"x{i}"] = tk.Entry(root, width=8)
            self.entries[f"y{i}"] = tk.Entry(root, width=8)
            self.entries[f"ra{i}"] = tk.Entry(root, width=12)
            self.entries[f"dec{i}"] = tk.Entry(root, width=12)

            self.entries[f"x{i}"].grid(row=i*2, column=1)
            self.entries[f"y{i}"].grid(row=i*2, column=2)
            self.entries[f"ra{i}"].grid(row=i*2, column=3)
            self.entries[f"dec{i}"].grid(row=i*2, column=4)

        # Checkbox for center calculation
        self.center_var = tk.IntVar()
        self.center_check = tk.Checkbutton(root, text="Calculate for center of image?", variable=self.center_var, command=self.toggle_inputs)
        self.center_check.grid(row=7, column=0, sticky='w')

        # Conditional fields for center or custom point
        tk.Label(root, text="Image Size (x, y):").grid(row=8, column=0, sticky='w')
        self.image_x = tk.Entry(root, width=8)
        self.image_y = tk.Entry(root, width=8)
        self.image_x.grid(row=8, column=1)
        self.image_y.grid(row=8, column=2)

        tk.Label(root, text="Point Coordinates (x, y):").grid(row=9, column=0, sticky='w')
        self.point_x = tk.Entry(root, width=8)
        self.point_y = tk.Entry(root, width=8)
        self.point_x.grid(row=9, column=1)
        self.point_y.grid(row=9, column=2)

        self.toggle_inputs()

        # Buttons
        self.calc_button = tk.Button(root, text="Calculate", command=self.perform_calculation)
        self.calc_button.grid(row=10, column=0, columnspan=2)

        self.save_button = tk.Button(root, text="Save Output", command=self.save_output)
        self.save_button.grid(row=10, column=2, columnspan=2)

        # Result display
        self.result_label = tk.Label(root, text="", justify='left')
        self.result_label.grid(row=11, column=0, columnspan=5)
        self.output_text = ""  # For saving results

    def toggle_inputs(self):
        if self.center_var.get():
            self.image_x.config(state="normal")
            self.image_y.config(state="normal")
            self.point_x.config(state="disabled")
            self.point_y.config(state="disabled")
        else:
            self.image_x.config(state="disabled")
            self.image_y.config(state="disabled")
            self.point_x.config(state="normal")
            self.point_y.config(state="normal")

    def perform_calculation(self):
        try:
            # Retrieve input data
            x1, y1 = float(self.entries["x1"].get()), float(self.entries["y1"].get())
            ra1, dec1 = deg_to_sec(self.entries["ra1"].get()), deg_to_sec(self.entries["dec1"].get())
            x2, y2 = float(self.entries["x2"].get()), float(self.entries["y2"].get())
            ra2, dec2 = deg_to_sec(self.entries["ra2"].get()), deg_to_sec(self.entries["dec2"].get())
            x3, y3 = float(self.entries["x3"].get()), float(self.entries["y3"].get())
            ra3, dec3 = deg_to_sec(self.entries["ra3"].get()), deg_to_sec(self.entries["dec3"].get())

            # Compute transformation coefficients
            a, b, c, d, e, f = calculate_transform(x1, y1, ra1, dec1, x2, y2, ra2, dec2, x3, y3, ra3, dec3)

            # Determine the point to calculate
            if self.center_var.get():
                x_new = center_of_coord(float(self.image_x.get()))
                y_new = center_of_coord(float(self.image_y.get()))
            else:
                x_new = float(self.point_x.get())
                y_new = float(self.point_y.get())

            # Calculate celestial coordinates
            ra_new, dec_new = transform_coordinates(a, b, c, d, e, f, x_new, y_new)
            ra_new = sec_to_deg(ra_new)
            dec_new = sec_to_deg(dec_new)

            self.output_text = f"RA: {ra_new}\nDec: {dec_new}"
            self.result_label.config(text=self.output_text)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def save_output(self):
        if not self.output_text:
            messagebox.showwarning("Warning", "No output to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.output_text)
            messagebox.showinfo("Success", "Output saved successfully!")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = StarFieldCalculator(root)
    root.mainloop()
