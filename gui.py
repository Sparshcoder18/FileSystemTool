import tkinter as tk
from tkinter import ttk
from file_system import FileSystem

fs = FileSystem()

# Ensure latest saved data is loaded
fs.load_file_table()

# ----------------------------
# MAIN WINDOW
# ----------------------------
root = tk.Tk()
root.title("File System Visualizer")
root.geometry("1000x600")

# ----------------------------
# LEFT PANEL (FILES)
# ----------------------------
left_frame = tk.Frame(root, width=200, bg="#1e1e1e")
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Files", fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=10)

file_list = tk.Listbox(left_frame)
file_list.pack(fill="both", expand=True, padx=10, pady=10)


# ----------------------------
# RIGHT PANEL (DETAILS)
# ----------------------------
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)

details_text = tk.Text(right_frame, height=10)
details_text.pack(fill="x", padx=10, pady=10)


# ----------------------------
# DISK VISUALIZATION
# ----------------------------
disk_frame = tk.Frame(right_frame)
disk_frame.pack(fill="both", expand=True, padx=10, pady=10)


def draw_disk():
    for widget in disk_frame.winfo_children():
        widget.destroy()

    for i in range(len(fs.disk.blocks)):
        if fs.disk.blocks[i] == "CORRUPTED":
            color = "red"
        elif fs.disk.bitmap[i] == 1:
            color = "green"
        else:
            color = "lightgray"

        block = tk.Label(
            disk_frame,
            text=str(i),
            bg=color,
            width=4,
            height=2,
            relief="ridge"
        )
        block.grid(row=i // 10, column=i % 10, padx=2, pady=2)


# ----------------------------
# FILE DETAILS DISPLAY
# ----------------------------
def show_details(event):
    selection = file_list.curselection()
    if not selection:
        return

    filename = file_list.get(selection[0])

    if filename not in fs.file_table:
        return

    info = fs.file_table[filename]

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, f"File: {filename}\n")
    details_text.insert(tk.END, f"Size: {info['size']} bytes\n")
    details_text.insert(tk.END, f"Blocks: {info['blocks']}\n")

file_list.bind("<<ListboxSelect>>", show_details)


# ----------------------------
# LOAD FILES
# ----------------------------
def load_files():
    file_list.delete(0, tk.END)

    if not fs.file_table:
        file_list.insert(tk.END, "No Files Found")
        return

    for file in fs.file_table:
        file_list.insert(tk.END, file)


# ----------------------------
# REFRESH BUTTON
# ----------------------------
refresh_btn = tk.Button(
    left_frame,
    text="Refresh",
    command=lambda: [load_files(), draw_disk()]
)
refresh_btn.pack(pady=10)

# ----------------------------
# ACTION BUTTONS
# ----------------------------
def create_file():
    fs.create_file("new_file")
    load_files()
    draw_disk()

def simulate_crash():
    fs.recovery.simulate_crash(fs.disk)
    draw_disk()

def recover():
    fs.recovery.recover(fs)
    load_files()
    draw_disk()

def defragment():
    fs.optimizer.defragment()
    draw_disk()


tk.Button(left_frame, text="Create File", command=create_file).pack(pady=5)
tk.Button(left_frame, text="Simulate Crash", command=simulate_crash).pack(pady=5)
tk.Button(left_frame, text="Recover", command=recover).pack(pady=5)
tk.Button(left_frame, text="Defragment", command=defragment).pack(pady=5)

# ----------------------------
# INITIAL LOAD
# ----------------------------
load_files()
draw_disk()

root.mainloop()