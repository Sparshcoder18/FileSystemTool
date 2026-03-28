import json
import os

# Constants
BLOCK_SIZE = 64          # size of each block (characters)
TOTAL_BLOCKS = 50        # total number of blocks (keep small for demo)

DATA_PATH = "data/disk_state.json"


class VirtualDisk:
    def __init__(self):
        self.blocks = [""] * TOTAL_BLOCKS
        self.bitmap = [0] * TOTAL_BLOCKS  # 0 = free, 1 = used
        self.load_disk()

    # ----------------------------
    # Load disk state from file
    # ----------------------------
    def load_disk(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r") as f:
                    data = json.load(f)
                    self.blocks = data.get("blocks", self.blocks)
                    self.bitmap = data.get("bitmap", self.bitmap)
            except:
                pass

    # ----------------------------
    # Save disk state to file
    # ----------------------------
    def save_disk(self):
        data = {
            "blocks": self.blocks,
            "bitmap": self.bitmap
        }
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

    # ----------------------------
    # Get free blocks
    # ----------------------------
    def get_free_blocks(self, n):
        free = [i for i in range(TOTAL_BLOCKS) if self.bitmap[i] == 0]
        return free[:n] if len(free) >= n else []

    # ----------------------------
    # Write data to blocks
    # ----------------------------
    def write_blocks(self, block_indices, data):
        chunks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

        if len(chunks) > len(block_indices):
            return False

        for i, block in enumerate(block_indices):
            if i < len(chunks):
                self.blocks[block] = chunks[i]
                self.bitmap[block] = 1

        self.save_disk()
        return True

    # ----------------------------
    # Read data from blocks
    # ----------------------------
    def read_blocks(self, block_indices):
        data = ""
        for block in block_indices:
            data += self.blocks[block]
        return data

    # ----------------------------
    # Free blocks
    # ----------------------------
    def free_blocks(self, block_indices):
        for block in block_indices:
            self.blocks[block] = ""
            self.bitmap[block] = 0

        self.save_disk()

    # ----------------------------
    # Display disk state
    # ----------------------------
    def display_disk(self):
        print("\n--- DISK STATE ---")
        for i in range(TOTAL_BLOCKS):
            status = "USED" if self.bitmap[i] else "FREE"
            print(f"Block {i}: {status} | Data: {self.blocks[i]}")

    # ----------------------------
    # Reset disk state
    # ----------------------------
    def reset_disk(self):
        self.blocks = [""] * TOTAL_BLOCKS
        self.bitmap = [0] * TOTAL_BLOCKS
        self.save_disk()