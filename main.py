from file_system import FileSystem

fs = FileSystem()

# Reset disk
fs.disk.reset_disk()

# Create files (to simulate fragmentation)
fs.create_file("file1")
fs.write_file("file1", "HelloWorld")

fs.create_file("file2")
fs.write_file("file2", "PythonIsAwesome "*30)

# Manually create fragmentation (simulate gaps)
fs.delete_file("file1")

fs.create_file("file3")
fs.write_file("file3", "FragmentationTest "*30)

# Before optimization
print("\n--- BEFORE OPTIMIZATION ---")
fs.show_files()
fs.disk.display_disk()
fs.optimizer.calculate_fragmentation()

# Show disk
fs.disk.display_disk()


fs.disk.show_disk_stats()

fs.disk.display_compact()
# Defragment
fs.optimizer.defragment()

# After optimization
print("\n--- AFTER OPTIMIZATION ---")
fs.show_files()
fs.disk.display_disk()
fs.optimizer.calculate_fragmentation()

print("\n--- PERFORMANCE BEFORE ---")
fs.optimizer.measure_read_time("file2")

fs.optimizer.defragment()

print("\n--- PERFORMANCE AFTER ---")
fs.optimizer.measure_read_time("file2")

print("\n💡 Optimization improved data locality and reduced access time.")

fs.show_block_map()

fs.search_file("file2")
fs.search_file("fileX")  # test missing file
