from disk import BLOCK_SIZE
import time


class OptimizationManager:
    def __init__(self, fs):
        self.fs = fs

    def calculate_fragmentation(self):
        fragmented = 0
        for f, info in self.fs.file_table.items():
            blocks = info["blocks"]
            if any(blocks[i]+1 != blocks[i+1] for i in range(len(blocks)-1)):
                fragmented += 1

        total = len(self.fs.file_table)
        if total:
            print(f"📉 Fragmentation: {(fragmented/total)*100:.2f}%")

    def defragment(self):
        print("⚡ Starting defragmentation...")

        new_blocks = [""]*len(self.fs.disk.blocks)
        new_bitmap = [0]*len(self.fs.disk.bitmap)
        ptr = 0
        new_table = {}

        for f, info in self.fs.file_table.items():
            data = self.fs.disk.read_blocks(info["blocks"])
            chunks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

            indices = []
            for chunk in chunks:
                new_blocks[ptr] = chunk
                new_bitmap[ptr] = 1
                indices.append(ptr)
                ptr += 1

            new_table[f] = {"blocks": indices, "size": len(data)}

        self.fs.disk.blocks = new_blocks
        self.fs.disk.bitmap = new_bitmap
        self.fs.file_table = new_table
        self.fs.disk.save_disk()
        self.fs.save_file_table()

        print("✔ Defragmentation completed.")

    def measure_read_time(self, filename):
        if filename not in self.fs.file_table:
            return
        start = time.time()
        self.fs.disk.read_blocks(self.fs.file_table[filename]["blocks"])
        print(f"⏱ Read Time: {(time.time()-start)*1000:.4f} ms")