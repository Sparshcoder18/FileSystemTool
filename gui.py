import tkinter as tk
from file_system import FileSystem

fs = FileSystem()
fs.load_file_table()

# ----------------------------
# MAIN WINDOW
# ----------------------------
root = tk.Tk()
root.title("File System Visualizer")
root.geometry("1100x650")

# ----------------------------
# LEFT PANEL
# ----------------------------
left_frame = tk.Frame(root, width=220, bg="#1e1e1e")
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Files", fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=10)

file_list = tk.Listbox(left_frame)
file_list.pack(fill="both", expand=True, padx=10, pady=10)

# ----------------------------
# INPUT SECTION
# ----------------------------
tk.Label(left_frame, text="Filename", fg="white", bg="#1e1e1e").pack()
file_entry = tk.Entry(left_frame)
file_entry.pack(pady=5)

tk.Label(left_frame, text="Data", fg="white", bg="#1e1e1e").pack()
data_entry = tk.Entry(left_frame)
data_entry.pack(pady=5)

# ----------------------------
# RIGHT PANEL
# ----------------------------
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)

details_text = tk.Text(right_frame, height=8)
details_text.pack(fill="x", padx=10, pady=10)

disk_frame = tk.Frame(right_frame)
disk_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ----------------------------
# BLOCK INFO DISPLAY (🔥 NEW)
# ----------------------------
def show_block_info(index):
    data = fs.disk.blocks[index]

    if data == "":
        status = "FREE"
    elif data == "CORRUPTED":
        status = "CORRUPTED"
    else:
        status = "USED"

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, f"Block Index: {index}\n")
    details_text.insert(tk.END, f"Status: {status}\n")
    details_text.insert(tk.END, f"Data:\n{data}")

# ----------------------------
# DISK DRAW (WITH CLICK + HIGHLIGHT)
# ----------------------------
def draw_disk(selected_blocks=None):
    for widget in disk_frame.winfo_children():
        widget.destroy()

    for i in range(len(fs.disk.blocks)):

        if fs.disk.blocks[i] == "CORRUPTED":
            color = "red"
        elif selected_blocks and i in selected_blocks:
            color = "blue"  # selected file blocks
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

        # 🔥 FIXED CLICK BINDING (no late binding bug)
        block.bind("<Button-1>", lambda e, idx=i: show_block_info(idx))

        block.grid(row=i // 10, column=i % 10, padx=2, pady=2)

# ----------------------------
# FILE DETAILS
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

    draw_disk(info["blocks"])

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
# BUTTON ACTIONS
# ----------------------------
def refresh():
    fs.load_file_table()
    load_files()
    draw_disk()

def create_file():
    name = file_entry.get().strip()
    if not name:
        return

    fs.create_file(name)
    load_files()
    draw_disk()

def write_file():
    name = file_entry.get().strip()
    data = data_entry.get().strip()

    if not name or not data:
        return

    fs.write_file(name, data)
    load_files()
    draw_disk()

def delete_file():
    name = file_entry.get().strip()
    if not name:
        return

    fs.delete_file(name)
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

# ----------------------------
# BUTTON UI
# ----------------------------
tk.Button(left_frame, text="Refresh", command=refresh).pack(pady=5)

tk.Button(left_frame, text="Create File", command=create_file).pack(pady=5)
tk.Button(left_frame, text="Write File", command=write_file).pack(pady=5)
tk.Button(left_frame, text="Delete File", command=delete_file).pack(pady=5)

tk.Button(left_frame, text="Simulate Crash", command=simulate_crash).pack(pady=5)
tk.Button(left_frame, text="Recover", command=recover).pack(pady=5)
tk.Button(left_frame, text="Defragment", command=defragment).pack(pady=5)

# ----------------------------
# INITIAL LOAD
# ----------------------------
load_files()
draw_disk()

root.mainloop()
