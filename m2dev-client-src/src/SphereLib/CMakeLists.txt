file(GLOB_RECURSE HEADER_FILES "*.h")
file(GLOB_RECURSE SOURCE_FILES "*.c" "*.cpp")

add_library(SphereLib STATIC
	${HEADER_FILES}
	${SOURCE_FILES}
)

# target_link_libraries(SphereLib
# )

source_group("Header Files" FILES ${HEADER_FILES})
source_group("Source Files" FILES ${SOURCE_FILES})
