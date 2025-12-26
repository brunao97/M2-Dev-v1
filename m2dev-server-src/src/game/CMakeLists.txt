file(GLOB_RECURSE GAME_SOURCES "*.h" "*.c" "*.cpp")

add_executable(game ${GAME_SOURCES})

target_compile_definitions(game PRIVATE GIT_DESCRIBE="${GIT_DESCRIBE_VERSION}")
set_target_properties(game PROPERTIES
	RUNTIME_OUTPUT_DIRECTORY "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/game"
	RUNTIME_OUTPUT_DIRECTORY_DEBUG "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/game"
	RUNTIME_OUTPUT_DIRECTORY_RELEASE "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/bin/game"
)

target_link_libraries(game 
	common 
	libgame 
	libpoly 
	libsql 
	libthecore 
	liblua

	# external
	mariadbclient
	cryptopp-static
)

if (WIN32)
	target_link_libraries(game ws2_32)
else()
	target_link_libraries(game pthread md)
endif()

# Copy to all runtime locations after build
add_custom_command(TARGET game POST_BUILD
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:game>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/game.exe"
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:game>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/channel1/core1/channel1_core1.exe"
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:game>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/channel1/core2/channel1_core2.exe"
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:game>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/channel1/core3/channel1_core3.exe"
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
		"$<TARGET_FILE:game>"
		"G:/metin2-files-clean-64/M2-Dev/m2dev-server/channels/channel99/core1/channel99_core1.exe"
	COMMENT "Copying game.exe to all server locations..."
)
