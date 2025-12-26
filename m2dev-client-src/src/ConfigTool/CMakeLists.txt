SET(ConfigTool_SOURCES
	main.cpp
)

ADD_EXECUTABLE(ConfigTool ${ConfigTool_SOURCES})

TARGET_LINK_LIBRARIES(ConfigTool
	EterLib
	GameLib
	EterPythonLib
	ScriptLib
	SphereLib
	EffectLib
	PRTerrainLib
	EterGrnLib
	EterImageLib
	SpeedTreeLib
	AudioLib
	EterBase
	EterLocale
	PackLib
)

SET_TARGET_PROPERTIES(ConfigTool PROPERTIES FOLDER "Tools")