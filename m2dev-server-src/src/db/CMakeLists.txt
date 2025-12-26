file(GLOB_RECURSE DB_SOURCES "*.h" "*.cpp")

add_executable(db ${DB_SOURCES})

target_compile_definitions(db PRIVATE GIT_DESCRIBE="${GIT_DESCRIBE_VERSION}")
set_target_properties(db PROPERTIES
	RUNTIME_OUTPUT_DIRECTORY "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/db"
	RUNTIME_OUTPUT_DIRECTORY_DEBUG "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/db"
	RUNTIME_OUTPUT_DIRECTORY_RELEASE "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/db"
)

target_link_libraries(db 
	common
	libgame 
	libpoly 
	libsql 
	libthecore

	# external
	mariadbclient
)

if (WIN32)
	target_link_libraries(db ws2_32)
else()
	target_link_libraries(db pthread md)
endif()

# Copy to channels/ folder after build
add_custom_command(TARGET db POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:db>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/db.exe"
	COMMENT "Copying db.exe to channels/ folder..."
)
