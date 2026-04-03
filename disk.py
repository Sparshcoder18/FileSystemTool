import json
import os

BLOCK_SIZE = 64
TOTAL_BLOCKS = 50

DATA_PATH = "data/disk_state.json"


class VirtualDisk:
    def __init__(self):
        self.blocks = [""] * TOTAL_BLOCKS
        self.bitmap = [0] * TOTAL_BLOCKS
        self.load_disk()

    def load_disk(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r") as f:
                    data = json.load(f)
                    self.blocks = data.get("blocks", self.blocks)
                    self.bitmap = data.get("bitmap", self.bitmap)
            except:
                pass

    def save_disk(self):
        os.makedirs("data", exist_ok=True)

        data = {
            "blocks": self.blocks,
            "bitmap": self.bitmap
        }
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def get_free_blocks(self, n):
        free = [i for i in range(TOTAL_BLOCKS) if self.bitmap[i] == 0]
        return free[:n] if len(free) >= n else []

    def write_blocks(self, block_indices, data):
        chunks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

        if len(chunks) > len(block_indices):
            return False

        for i, block in enumerate(block_indices):
            self.blocks[block] = chunks[i]
            self.bitmap[block] = 1

        self.save_disk()
        return True

    def read_blocks(self, block_indices):
        return "".join(self.blocks[b] for b in block_indices)

    def free_blocks(self, block_indices):
        for block in block_indices:
            self.blocks[block] = ""
            self.bitmap[block] = 0
        self.save_disk()

    def display_disk(self):
        print("\n--- DISK STATE ---")
        for i in range(TOTAL_BLOCKS):
            status = "USED" if self.bitmap[i] else "FREE"
            print(f"Block {i}: {status} | Data: {self.blocks[i]}")

    def reset_disk(self):
        self.blocks = [""] * TOTAL_BLOCKS
        self.bitmap = [0] * TOTAL_BLOCKS
        self.save_disk()

    def display_compact(self):
        print("\n--- COMPACT DISK VIEW ---")
        for i in range(len(self.blocks)):
            print(f"[{i}:{'USED' if self.bitmap[i] else 'FREE'}]", end=" ")
        print()

    def show_disk_stats(self):
        total = len(self.blocks)
        used = sum(self.bitmap)
        free = total - used

        print("\n--- DISK STATS ---")
        print(f"Total Blocks: {total}")
        print(f"Used Blocks: {used}")
        print(f"Free Blocks: {free}")
        print(f"Usage: {(used/total)*100:.2f}%")