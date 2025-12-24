# Collect all source files from the current directory
file(GLOB_RECURSE DUMP_PROTO_SOURCES "*.h" "*.cpp")

# Add an executable target for the project, using all the collected files.
add_executable(dump_proto ${DUMP_PROTO_SOURCES})

# Link the executable to the LZO static library.
# The `lzo2` target is created by the `lzo_2.10/CMakeLists.txt` file.
target_link_libraries(dump_proto PRIVATE lzo2)