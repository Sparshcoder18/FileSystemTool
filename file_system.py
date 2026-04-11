from recovery import RecoveryManager
from disk import VirtualDisk
from optimization import OptimizationManager
from disk import BLOCK_SIZE
class FileSystem:
    def __init__(self):
        self.disk = VirtualDisk()
        self.recovery = RecoveryManager()
        self.file_table = {}  # filename → {"blocks": [], "size": int}
        self.optimizer = OptimizationManager(self)

    # ----------------------------
    # Create File
    # ----------------------------
    def create_file(self, filename):
        if filename in self.file_table:
            print("File already exists.")
            return

        self.file_table[filename] = {"blocks": [], "size": 0}
        print(f"File '{filename}' created.")

    # ----------------------------
    # Write File
    # ----------------------------
    def write_file(self, filename, data):
        self.recovery.log(f"WRITE|{filename}|{data}")
        
        if filename not in self.file_table:
            print("File does not exist.")
            return

        self.recovery.log(f"WRITE|{filename}|{data}")

        # Free old blocks if rewriting
        old_blocks = self.file_table[filename]["blocks"]
        if old_blocks:
            self.disk.free_blocks(old_blocks)

        # Calculate required blocks
        BLOCK_SIZE = 64
        required_blocks = (len(data) // BLOCK_SIZE) + (1 if len(data) % BLOCK_SIZE else 0)

        blocks = self.disk.get_free_blocks(required_blocks)

        if not blocks:
            print("Not enough space.")
            return

        success = self.disk.write_blocks(blocks, data)

        if success:
            self.file_table[filename]["blocks"] = blocks
            self.file_table[filename]["size"] = len(data)
            print(f"Data written to '{filename}'.")

    # ----------------------------
    # Read File
    # ----------------------------
    def read_file(self, filename):
        if filename not in self.file_table:
            print("File not found.")
            return

        blocks = self.file_table[filename]["blocks"]
        data = self.disk.read_blocks(blocks)

        print(f"Data in '{filename}': {data}")

    # ----------------------------
    # Delete File
    # ----------------------------
    def delete_file(self, filename):
        if filename not in self.file_table:
            print("File not found.")
            return

        blocks = self.file_table[filename]["blocks"]
        self.disk.free_blocks(blocks)

        del self.file_table[filename]
        print(f"File '{filename}' deleted.")

    # ----------------------------
    # Show File Table
    # ----------------------------
    def show_files(self):
        print("\n--- FILE TABLE ---")
        for name, info in self.file_table.items():
            print(f"{name} → Blocks: {info['blocks']} | Size: {info['size']} bytes")

    # ----------------------------
    # Show Block Mapping
    # ----------------------------
    def show_block_map(self):
        print("\n--- BLOCK MAP ---")
        for file, blocks in self.file_table.items():
            print(f"{file} -> {blocks}")
