file(GLOB_RECURSE QC_SOURCES "*.h" "*.cpp")

add_executable(qc ${QC_SOURCES})
set_target_properties(qc PROPERTIES
	RUNTIME_OUTPUT_DIRECTORY "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/locale/english/quest"
	RUNTIME_OUTPUT_DIRECTORY_DEBUG "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/locale/english/quest"
	RUNTIME_OUTPUT_DIRECTORY_RELEASE "G:/metin2-files-clean-64/M2-Dev/m2dev-server/share/locale/english/quest"
)

target_link_libraries(qc 
	liblua 
)

if (WIN32)
	target_link_libraries(qc ws2_32)
else()
	target_link_libraries(qc pthread md)
endif()
