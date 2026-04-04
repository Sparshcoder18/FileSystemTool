import tkinter as tk
from tkinter import ttk
from file_system import FileSystem

fs = FileSystem()
fs.load_file_table()

# ----------------------------
# WINDOW
# ----------------------------
root = tk.Tk()
root.title("File System Dashboard")
root.geometry("1200x720")
root.configure(bg="#f4f6f8")

# ----------------------------
# COLORS
# ----------------------------
PRIMARY = "#3b82f6"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
GRAY = "#e5e7eb"
CARD = "white"

# ----------------------------
# HEADER
# ----------------------------
tk.Label(root,
         text="File System Simulation Dashboard",
         font=("Segoe UI", 18, "bold"),
         bg="#f4f6f8").pack(pady=10)

# ----------------------------
# CONTROL PANEL
# ----------------------------
control = tk.Frame(root, bg=CARD, bd=1, relief="solid")
control.pack(fill="x", padx=10, pady=5)

tk.Label(control, text="File Name", bg=CARD).grid(row=0, column=0, padx=5)
file_entry = tk.Entry(control, width=20)
file_entry.grid(row=0, column=1, padx=5)

tk.Label(control, text="Data", bg=CARD).grid(row=0, column=2, padx=5)

data_entry = tk.Text(
    control,
    height=3,
    width=100,
    bd=1,
    relief="solid",
    highlightbackground="#d1d5db",
    highlightcolor="#d1d5db",
    highlightthickness=1,
    wrap="word"
)
data_entry.grid(row=0, column=3, padx=5, sticky="ew")

# Buttons
btn_frame = tk.Frame(control, bg=CARD)
btn_frame.grid(row=1, column=0, columnspan=4, pady=5)

buttons = []

# ----------------------------
# MAIN AREA
# ----------------------------
main = tk.Frame(root, bg="#f4f6f8")
main.pack(fill="both", expand=True, padx=10, pady=5)

main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=2)

# ----------------------------
# FILE PANEL
# ----------------------------
file_panel = tk.Frame(main, bg=CARD, bd=1, relief="solid")
file_panel.grid(row=0, column=0, sticky="nsew", padx=5)

tk.Label(file_panel, text="Files", font=("Segoe UI", 12, "bold"),
         bg=CARD).pack(anchor="w", padx=10, pady=5)

tree = ttk.Treeview(file_panel, columns=("size", "blocks"))

tree.heading("#0", text="File Name")
tree.heading("size", text="Size")
tree.heading("blocks", text="Blocks")

tree.column("#0", width=120)
tree.column("size", width=60)
tree.column("blocks", width=140)

tree.pack(fill="both", expand=True, padx=10, pady=10)

# ----------------------------
# RIGHT PANEL (DETAIL + DISK)
# ----------------------------
right_panel = tk.Frame(main, bg=CARD, bd=1, relief="solid")
right_panel.grid(row=0, column=1, sticky="nsew", padx=5)

# DETAILS
details = tk.Text(right_panel, height=6)
details.pack(fill="x", padx=10, pady=5)

# DISK GRID
disk_frame = tk.Frame(right_panel, bg=CARD)
disk_frame.pack(pady=10)

legend_frame = tk.Frame(right_panel, bg=CARD)
legend_frame.pack(pady=8)

def legend_item(color, text):
    item = tk.Frame(legend_frame, bg=CARD)
    item.pack(side="left", padx=10)

    box = tk.Label(item, bg=color, width=2, height=1, bd=1, relief="solid")
    box.pack(side="left", padx=3)

    tk.Label(item, text=text, bg=CARD).pack(side="left")

legend_item("green", "Used")
legend_item("#e5e7eb", "Free")
legend_item("#ef4444", "Corrupted")
legend_item("#3b82f6", "Selected")

# ----------------------------
# ACTIVITY LOG (FIXED)
# ----------------------------
log_panel = tk.Frame(root, bg=CARD, bd=1, relief="solid")
log_panel.pack(fill="x", padx=10, pady=5)

tk.Label(log_panel, text="Activity Log",
         font=("Segoe UI", 11, "bold"),
         bg=CARD).pack(anchor="w", padx=10)

log_box = tk.Text(log_panel, height=5)
log_box.pack(fill="x", padx=10, pady=5)

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# ----------------------------
# SHOW BLOCK INFO
# ----------------------------
def show_block_info(index):
    data = fs.disk.blocks[index]

    status = "FREE"
    if data == "CORRUPTED":
        status = "CORRUPTED"
    elif fs.disk.bitmap[index] == 1:
        status = "USED"

    details.delete("1.0", tk.END)
    details.insert(tk.END,
        f"Block: {index}\n"
        f"Status: {status}\n"
        f"Size: {len(data)} chars\n\n"
        f"{data}"
    )

# ----------------------------
# DRAW DISK
# ----------------------------
def draw_disk(selected=None):
    for w in disk_frame.winfo_children():
        w.destroy()

    for i in range(len(fs.disk.blocks)):

        block_data = fs.disk.blocks[i]

        # COLOR LOGIC
        if block_data == "CORRUPTED":
            color = "#ef4444"
        elif fs.disk.bitmap[i] == 1:
            color = "green"
        else:
            color = "#e5e7eb"

        # 🔥 GLOW EFFECT FOR SELECTED
        border_width = 2
        border_color = "black"

        if selected and i in selected:
            color = "#3b82f6"
            border_width = 4
            border_color = "#2563eb"

        b = tk.Label(
            disk_frame,
            text=i,
            bg=color,
            width=4,
            height=2,
            relief="solid",
            bd=border_width,
            highlightbackground=border_color,
            highlightthickness=border_width,
            cursor="hand2"
        )

        # CLICK
        b.bind("<Button-1>", lambda e, idx=i: [
            show_block_info(idx),
            draw_disk([idx])
        ])

        # HOVER
        b.bind("<Enter>", lambda e, w=b: w.config(relief="raised"))
        b.bind("<Leave>", lambda e, w=b: w.config(relief="solid"))

        b.grid(row=i//10, column=i%10, padx=3, pady=3)

# ----------------------------
# LOAD FILES
# ----------------------------
def load_files():
    for i in tree.get_children():
        tree.delete(i)

    for f, info in fs.file_table.items():
        tree.insert("", "end", text=f,
                    values=(info["size"], info["blocks"]))

# ----------------------------
# SELECT FILE
# ----------------------------
def on_select(e):
    item = tree.focus()
    if not item:
        return

    f = tree.item(item, "text")
    info = fs.file_table[f]

    details.delete("1.0", tk.END)
    details.insert(tk.END,
        f"File: {f}\nSize: {info['size']}\nBlocks: {info['blocks']}")

    draw_disk(info["blocks"])

tree.bind("<<TreeviewSelect>>", on_select)

# ----------------------------
# ACTIONS
# ----------------------------
def create():
    name = file_entry.get()
    if not name:
        return
    fs.create_file(name)
    log(f"Created: {name}")
    load_files()
    draw_disk()

def animate_write(blocks):
    for i, block_index in enumerate(blocks):

        def step(idx=block_index):
            widgets = disk_frame.winfo_children()

            if idx < len(widgets):
                w = widgets[idx]

                # 🔥 yellow = writing
                w.config(bg="#facc15")
                root.update()

                # after delay → green
                root.after(150, lambda: w.config(bg="green"))

        root.after(i * 120, step)

def write():
    name = file_entry.get()
    data = data_entry.get("1.0", tk.END).strip()
    if not name or not data:
        return
    fs.write_file(name, data)
    log(f"Wrote: {name}")

    # 🔥 animate written blocks
    blocks = fs.file_table[name]["blocks"]
    animate_write(blocks)

    load_files()
    draw_disk()

def delete():
    name = file_entry.get()
    if not name:
        return
    fs.delete_file(name)
    log(f"Deleted: {name}")
    load_files()
    draw_disk()

def crash():
    fs.recovery.simulate_crash(fs.disk)
    log("Crash simulated")
    draw_disk()

def recover():
    fs.recovery.recover(fs)
    log("Recovered")
    load_files()
    draw_disk()

def defrag():
    fs.optimizer.defragment()
    log("Defragmented")
    draw_disk()

# ----------------------------
# BUTTONS
# ----------------------------
btns = [
    ("Create", create),
    ("Write", write),
    ("Delete", delete),
    ("Crash", crash),
    ("Recover", recover),
    ("Defrag", defrag)
]

for text, cmd in btns:
    tk.Button(btn_frame, text=text, command=cmd,
              bg=PRIMARY, fg="white", width=10).pack(side="left", padx=5)

# ----------------------------
# INIT
# ----------------------------
load_files()
draw_disk()

root.mainloop()