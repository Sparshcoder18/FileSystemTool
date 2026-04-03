from file_system import FileSystem

fs = FileSystem()
fs.disk.reset_disk()

# ----------------------------
# CREATE FILES
# ----------------------------
fs.create_file("file1")
fs.write_file("file1", "HelloWorld")

fs.create_file("file2")
fs.write_file("file2", "PythonIsAwesome " * 30)

fs.delete_file("file1")

fs.create_file("file3")
fs.write_file("file3", "FragmentationTest " * 30)

# ----------------------------
# BEFORE OPTIMIZATION
# ----------------------------
print("\n--- BEFORE OPTIMIZATION ---")
fs.show_files()
fs.disk.display_disk()
fs.optimizer.calculate_fragmentation()

fs.disk.show_disk_stats()
fs.disk.display_compact()

# ----------------------------
# CRASH SIMULATION
# ----------------------------
print("\n--- SIMULATING CRASH ---")
fs.recovery.simulate_crash(fs.disk)

print("\n--- RECOVERY ---")
fs.recovery.recover(fs)

print("\n--- AFTER RECOVERY ---")
fs.show_files()
fs.disk.display_disk()

# ----------------------------
# PERFORMANCE BEFORE
# ----------------------------
print("\n--- PERFORMANCE BEFORE ---")
fs.optimizer.measure_read_time("file2")

# ----------------------------
# DEFRAGMENTATION
# ----------------------------
fs.optimizer.defragment()

# ----------------------------
# AFTER OPTIMIZATION
# ----------------------------
print("\n--- AFTER OPTIMIZATION ---")
fs.show_files()
fs.disk.display_disk()
fs.optimizer.calculate_fragmentation()

# ----------------------------
# PERFORMANCE AFTER
# ----------------------------
print("\n--- PERFORMANCE AFTER ---")
fs.optimizer.measure_read_time("file2")

# ----------------------------
# PERSISTENCE CHECK
# ----------------------------
print("\n--- RELOADING SYSTEM ---")
fs2 = FileSystem()
fs2.show_files()

# ----------------------------
# RESET
# ----------------------------
fs.disk.reset_disk()

# 🔥 ADD THIS
fs.file_table = {}
fs.save_file_table()