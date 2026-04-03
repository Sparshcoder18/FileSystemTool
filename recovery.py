import os
import random

LOG_PATH = "logs/journal.log"


class RecoveryManager:
    def __init__(self):
        self.log_path = LOG_PATH
        os.makedirs("logs", exist_ok=True)

    # ----------------------------
    # Log operation (WAL)
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
        block = random.randint(0, len(disk.blocks) - 1)

        disk.blocks[block] = "CORRUPTED"
        disk.bitmap[block] = 1  # mark as used

        disk.save_disk()

        print(f"⚠ Crash simulated! Block {block} corrupted.")

    # ----------------------------
    # Recover system
    # ----------------------------
    def recover(self, file_system):
        print("🔄 Recovery started...")

        logs = self.read_logs()

        # 🔥 STEP 1: Clean corrupted blocks FIRST
        for i in range(len(file_system.disk.blocks)):
            if file_system.disk.blocks[i] == "CORRUPTED":
                file_system.disk.blocks[i] = ""
                file_system.disk.bitmap[i] = 0

        # 🔥 STEP 2: Reset file table (VERY IMPORTANT)
        file_system.file_table = {}
        file_system.save_file_table()

        # 🔥 STEP 3: Replay logs (redo operations)
        for entry in logs:
            entry = entry.strip().split("|")

            if entry[0] == "WRITE":
                filename = entry[1]
                data = entry[2]

                # Recreate file if missing
                if filename not in file_system.file_table:
                    file_system.create_file(filename)

                file_system.write_file(filename, data, log=False)

        # 🔥 STEP 4: Save final disk + metadata
        file_system.disk.save_disk()
        file_system.save_file_table()

        # 🔥 STEP 5: Clear logs (commit)
        self.clear_logs()

        print("✔ Recovery completed.")