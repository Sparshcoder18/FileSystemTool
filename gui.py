import tkinter as tk
from tkinter import ttk
from file_system import FileSystem

fs = FileSystem()
fs.load_file_table()

# ----------------------------
# MAIN WINDOW
# ----------------------------
root = tk.Tk()
root.title("File System Visualizer")
root.geometry("1200x700")

# ----------------------------
# TOP TITLE
# ----------------------------
title = tk.Label(root, text="File System Recovery & Optimization Simulator",
                 font=("Arial", 16, "bold"))
title.pack(pady=5)

# ----------------------------
# TOOLBAR
# ----------------------------
toolbar = tk.Frame(root)
toolbar.pack(fill="x", pady=5)

file_entry = tk.Entry(toolbar, width=20)
file_entry.insert(0, "filename")
file_entry.pack(side="left", padx=5)

data_entry = tk.Entry(toolbar, width=40)
data_entry.insert(0, "data")
data_entry.pack(side="left", padx=5)

# ----------------------------
# MAIN SPLIT
# ----------------------------
main_frame = tk.PanedWindow(root)
main_frame.pack(fill="both", expand=True)

# ----------------------------
# LEFT: FILE TABLE
# ----------------------------
left_frame = tk.Frame(main_frame)
main_frame.add(left_frame, width=350)

tk.Label(left_frame, text="Files (File Table)", font=("Arial", 12, "bold")).pack()

tree = ttk.Treeview(left_frame, columns=("name", "size", "blocks"), show="headings")
tree.heading("name", text="Filename")
tree.heading("size", text="Size")
tree.heading("blocks", text="Blocks")

tree.column("name", width=100)
tree.column("size", width=80)
tree.column("blocks", width=150)

tree.pack(fill="both", expand=True)

# ----------------------------
# RIGHT: DETAILS + DISK
# ----------------------------
right_frame = tk.Frame(main_frame)
main_frame.add(right_frame)

# DETAILS
tk.Label(right_frame, text="Details / Block Info", font=("Arial", 12, "bold")).pack()

details_text = tk.Text(right_frame, height=6)
details_text.pack(fill="x", padx=10, pady=5)

# DISK LABEL
tk.Label(right_frame, text="Disk Blocks (Visualization)", font=("Arial", 12, "bold")).pack()

disk_frame = tk.Frame(right_frame)
disk_frame.pack(pady=10)

# LEGEND
legend = tk.Label(right_frame,
    text="🟩 Used   ⬜ Free   🟥 Corrupted   🟦 Selected File",
    font=("Arial", 10))
legend.pack()

# ----------------------------
# STATUS BAR
# ----------------------------
status = tk.Label(root, text="Ready", bd=1, relief="sunken", anchor="w")
status.pack(fill="x", side="bottom")

# ----------------------------
# BLOCK INFO
# ----------------------------
def show_block_info(index):
    data = fs.disk.blocks[index]

    if data == "":
        status_txt = "FREE"
    elif data == "CORRUPTED":
        status_txt = "CORRUPTED"
    else:
        status_txt = "USED"

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END,
        f"Block Index: {index}\nStatus: {status_txt}\n\nData:\n{data}"
    )

# ----------------------------
# DRAW DISK
# ----------------------------
def draw_disk(selected_blocks=None):
    for widget in disk_frame.winfo_children():
        widget.destroy()

    for i in range(len(fs.disk.blocks)):

        if fs.disk.blocks[i] == "CORRUPTED":
            color = "red"
        elif selected_blocks and i in selected_blocks:
            color = "blue"
        elif fs.disk.bitmap[i] == 1:
            color = "green"
        else:
            color = "lightgray"

        block = tk.Label(disk_frame, text=str(i), bg=color, width=4, height=2)
        block.bind("<Button-1>", lambda e, idx=i: show_block_info(idx))
        block.grid(row=i // 10, column=i % 10, padx=2, pady=2)

# ----------------------------
# LOAD FILES
# ----------------------------
def load_files():
    for row in tree.get_children():
        tree.delete(row)

    for file, info in fs.file_table.items():
        tree.insert("", "end", values=(file, info["size"], str(info["blocks"])))

    update_status()

# ----------------------------
# FILE SELECT
# ----------------------------
def on_select(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    filename = values[0]

    info = fs.file_table[filename]

    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END,
        f"File: {filename}\nSize: {info['size']} bytes\nBlocks: {info['blocks']}"
    )

    draw_disk(info["blocks"])

tree.bind("<<TreeviewSelect>>", on_select)

# ----------------------------
# STATUS UPDATE
# ----------------------------
def update_status():
    used = sum(fs.disk.bitmap)
    total = len(fs.disk.bitmap)

    status.config(
        text=f"Files: {len(fs.file_table)} | Used Blocks: {used}/{total}"
    )

# ----------------------------
# ACTIONS
# ----------------------------
def create_file():
    name = file_entry.get().strip()
    fs.create_file(name)
    load_files()
    draw_disk()

def write_file():
    name = file_entry.get().strip()
    data = data_entry.get().strip()
    fs.write_file(name, data)
    load_files()
    draw_disk()

def delete_file():
    name = file_entry.get().strip()
    fs.delete_file(name)
    load_files()
    draw_disk()

def crash():
    fs.recovery.simulate_crash(fs.disk)
    draw_disk()

def recover():
    fs.recovery.recover(fs)
    load_files()
    draw_disk()

def defrag():
    fs.optimizer.defragment()
    draw_disk()

# ----------------------------
# BUTTONS
# ----------------------------
tk.Button(toolbar, text="Create", command=create_file).pack(side="left")
tk.Button(toolbar, text="Write", command=write_file).pack(side="left")
tk.Button(toolbar, text="Delete", command=delete_file).pack(side="left")
tk.Button(toolbar, text="Crash", command=crash).pack(side="left")
tk.Button(toolbar, text="Recover", command=recover).pack(side="left")
tk.Button(toolbar, text="Defrag", command=defrag).pack(side="left")

# ----------------------------
# INIT
# ----------------------------
load_files()
draw_disk()

root.mainloop()
