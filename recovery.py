import os
from disk import BLOCK_SIZE

LOG_PATH = "logs/journal.log"


class RecoveryManager:
    def __init__(self):
        self.log_path = LOG_PATH

    # ----------------------------
    # Log operation
    # ----------------------------
    def log(self, operation):
        with open(self.log_path, "a") as f:
            f.write(operation + "\n")

    # ----------------------------
    # Read logs
    # ----------------------------
    def read_logs(self):
        if not os.path.exists(self.log_path):
            return []

        with open(self.log_path, "r") as f:
            return f.readlines()

    # ----------------------------
    # Clear logs
    # ----------------------------
    def clear_logs(self):
        open(self.log_path, "w").close()

    # ----------------------------
    # Simulate crash
    # ----------------------------
    def simulate_crash(self, disk):
        import random
        block = random.randint(0, len(disk.blocks) - 1)

        disk.blocks[block] = "CORRUPTED"
        disk.bitmap[block] = 1   # mark as used (important)
        disk.save_disk()

        print(f"⚠ Crash simulated! Block {block} corrupted.")

    # ----------------------------
    # Recover system
    # ----------------------------
    def recover(self, file_system):
        print("🔄 Recovery started...")

        logs = self.read_logs()

        # 🔹 Step 1: Replay logs
        for entry in logs:
            entry = entry.strip().split("|")

            if entry[0] == "WRITE":
                filename = entry[1]
                data = entry[2]

                file_system.write_file(filename, data)

        # 🔹 Step 2: Clean corrupted blocks
        for i in range(len(file_system.disk.blocks)):
            if file_system.disk.blocks[i] == "CORRUPTED":
                file_system.disk.blocks[i] = ""
                file_system.disk.bitmap[i] = 0

        # 🔹 Step 3: Save cleaned disk state
        file_system.disk.save_disk()

        # 🔹 Step 4: Clear logs
        self.clear_logs()

        print("✔ Recovery completed.")