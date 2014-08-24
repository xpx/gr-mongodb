INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MONGODB mongodb)

FIND_PATH(
    MONGODB_INCLUDE_DIRS
    NAMES mongodb/api.h
    HINTS $ENV{MONGODB_DIR}/include
        ${PC_MONGODB_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MONGODB_LIBRARIES
    NAMES gnuradio-mongodb
    HINTS $ENV{MONGODB_DIR}/lib
        ${PC_MONGODB_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MONGODB DEFAULT_MSG MONGODB_LIBRARIES MONGODB_INCLUDE_DIRS)
MARK_AS_ADVANCED(MONGODB_LIBRARIES MONGODB_INCLUDE_DIRS)

