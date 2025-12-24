file(GLOB_RECURSE HEADER_FILES "*.h")
file(GLOB_RECURSE SOURCE_FILES "*.c" "*.cpp")

add_executable(UserInterface WIN32
	${HEADER_FILES}
	${SOURCE_FILES}
	${CMAKE_SOURCE_DIR}/src/UserInterface/UserInterface.rc
)

set_target_properties(UserInterface PROPERTIES
	LINK_FLAGS "/level='requireAdministrator' /uiAccess='false'"
	RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
	OUTPUT_NAME_DEBUG "Metin2_Debug"
	OUTPUT_NAME_RELEASE "Metin2_Release"
	OUTPUT_NAME_RELWITHDEBINFO "Metin2_RelWithDebInfo"
)

target_link_libraries(UserInterface
	AudioLib
	EffectLib
	EterBase
	EterGrnLib
	EterImageLib
	EterLib
	EterLocale
	EterPythonLib
	GameLib
	PRTerrainLib
	ScriptLib
	SpeedTreeLib
	SphereLib
	PackLib

	cryptopp-static
	lzo2
	libzstd_static
	mio

	DirectX
	Granny
	SpeedTree
	Python
	WebView

	ws2_32
	strmiids
	amstrmid
	dmoguids
	ddraw
	version
	Dbghelp
)

source_group("Header Files" FILES ${HEADER_FILES})
source_group("Source Files" FILES ${SOURCE_FILES})
