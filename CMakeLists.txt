
IF (BUILD_GUI)
    PYSIDE_WRAP_RC(JunkRig_QRC_SRCS Resources/JunkRig.qrc)
ENDIF (BUILD_GUI)

SET(JunkRig_SRCS
    Init.py
    InitGui.py
    JunkRig.py
    JunkRigGui.py
)
SOURCE_GROUP("" FILES ${JunkRig_SRCS})

ADD_CUSTOM_TARGET(JunkRig ALL
    SOURCES ${JunkRig_SRCS} ${JunkRig_QRC_SRCS}
)

fc_copy_sources(JunkRig "${CMAKE_BINARY_DIR}/Mod/JunkRig" ${JunkRig_SRCS})

IF (BUILD_GUI)
    fc_target_copy_resource(JunkRig
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_BINARY_DIR}/Mod/JunkRig
        JunkRig_rc.py)
ENDIF (BUILD_GUI)

INSTALL(
    FILES
        ${JunkRig_SRCS}
        ${JunkRig_QRC_SRCS}
    DESTINATION
        Mod/JunkRig
)

SET(JunkRigGuiIcon_SVG
    Resources/icons/JunkRigWorkbench.svg
)

fc_copy_sources(JunkRig "${CMAKE_BINARY_DIR}/Mod/JunkRig" ${JunkRigGuiIcon_SVG})
INSTALL(FILES ${JunkRigGuiIcon_SVG} DESTINATION "Mod/JunkRig/Resources/icons")
