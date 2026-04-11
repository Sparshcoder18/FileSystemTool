from disk import BLOCK_SIZE
import time


class OptimizationManager:
    def __init__(self, file_system):
        self.fs = file_system

    # ----------------------------
    # Calculate Fragmentation
    # ----------------------------
    def calculate_fragmentation(self):
        fragmented_files = 0

        for file, info in self.fs.file_table.items():
            blocks = info["blocks"]

            if len(blocks) <= 1:
                continue

            sorted_blocks = sorted(blocks)

            for i in range(len(sorted_blocks) - 1):
                if sorted_blocks[i] + 1 != sorted_blocks[i + 1]:
                    fragmented_files += 1
                    break

        total_files = len(self.fs.file_table)

        if total_files == 0:
            print("No files present.")
            return

        fragmentation_percent = (fragmented_files / total_files) * 100
        print(f"📉 Fragmentation: {fragmentation_percent:.2f}%")

    # ----------------------------
    # Defragmentation
    # ----------------------------
    def defragment(self):
        print("⚡ Starting defragmentation...")

        new_blocks = [""] * len(self.fs.disk.blocks)
        new_bitmap = [0] * len(self.fs.disk.bitmap)

        current_block = 0
        new_file_table = {}

        for file, info in self.fs.file_table.items():
            blocks = info["blocks"]
            data = self.fs.disk.read_blocks(blocks)

            chunks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

            new_indices = []

            for chunk in chunks:
                if current_block >= len(new_blocks):
                    print("Disk overflow during defragmentation!")
                    return

                new_blocks[current_block] = chunk
                new_bitmap[current_block] = 1
                new_indices.append(current_block)
                current_block += 1

            new_file_table[file] = {
                "blocks": new_indices,
                "size": len(data)
            }

        # Apply changes
        self.fs.disk.blocks = new_blocks
        self.fs.disk.bitmap = new_bitmap
        self.fs.file_table = new_file_table

        self.fs.disk.save_disk()

        print("✔ Defragmentation completed.")

    # ----------------------------
    # Measure Read Performance
    # ----------------------------
    def measure_read_time(self, filename):
        if filename not in self.fs.file_table:
            print("File not found.")
            return

        blocks = self.fs.file_table[filename]["blocks"]

        start = time.time()
        self.fs.disk.read_blocks(blocks)
        end = time.time()

        print(f"⏱ Read Time for {filename}: {(end - start)*1000:.4f} ms")