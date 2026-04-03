import json
import os
from disk import VirtualDisk, BLOCK_SIZE
from recovery import RecoveryManager
from optimization import OptimizationManager

FILE_TABLE_PATH = "data/file_table.json"


class FileSystem:
    def __init__(self):
        self.disk = VirtualDisk()
        self.recovery = RecoveryManager()
        self.file_table = {}
        self.load_file_table()
        self.optimizer = OptimizationManager(self)

    def save_file_table(self):
        os.makedirs("data", exist_ok=True)
        with open(FILE_TABLE_PATH, "w") as f:
            json.dump(self.file_table, f, indent=4)

    def load_file_table(self):
        if os.path.exists(FILE_TABLE_PATH):
            with open(FILE_TABLE_PATH, "r") as f:
                self.file_table = json.load(f)

    def create_file(self, filename):
        if filename in self.file_table:
            print("File already exists.")
            return
        self.file_table[filename] = {"blocks": [], "size": 0}
        self.save_file_table()
        print(f"File '{filename}' created.")

    def write_file(self, filename, data,  log=True):
        if filename not in self.file_table:
            print("File does not exist.")
            return

        self.recovery.log(f"WRITE|{filename}|{data}")

        old_blocks = self.file_table[filename]["blocks"]
        if old_blocks:
            self.disk.free_blocks(old_blocks)

        required_blocks = (len(data)//BLOCK_SIZE) + (1 if len(data)%BLOCK_SIZE else 0)
        blocks = self.disk.get_free_blocks(required_blocks)

        if not blocks:
            print("Not enough space.")
            return

        if self.disk.write_blocks(blocks, data):
            self.file_table[filename] = {"blocks": blocks, "size": len(data)}
            self.save_file_table()
            print(f"Data written to '{filename}'.")

    def read_file(self, filename):
        if filename not in self.file_table:
            print("File not found.")
            return
        data = self.disk.read_blocks(self.file_table[filename]["blocks"])
        print(f"Data in '{filename}': {data}")

    def delete_file(self, filename):
        if filename not in self.file_table:
            print("File not found.")
            return
        self.disk.free_blocks(self.file_table[filename]["blocks"])
        del self.file_table[filename]
        self.save_file_table()
        print(f"File '{filename}' deleted.")

    def show_files(self):
        print("\n--- FILE TABLE ---")
        for f, info in self.file_table.items():
            print(f"{f} → Blocks: {info['blocks']} | Size: {info['size']} bytes")

    def show_block_map(self):
        print("\n--- BLOCK MAP ---")
        for f, info in self.file_table.items():
            print(f"{f} -> {info['blocks']}")

    def append_file(self, filename, data):
        if filename not in self.file_table:
            print("File not found.")
            return
        old_data = self.disk.read_blocks(self.file_table[filename]["blocks"])
        self.write_file(filename, old_data + data)