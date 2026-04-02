from file_system import FileSystem

fs = FileSystem()

# Create file
fs.create_file("file1")

# Write data
fs.write_file("file1", "HelloWorld")

# Read data
fs.read_file("file1")

# Show file table
fs.show_files()

# Show disk
fs.disk.display_disk()

fs.disk.display_compact()