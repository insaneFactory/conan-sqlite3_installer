cmake_minimum_required(VERSION 3.1.2)
project(sqlite3 C)

include(conanbuildinfo.cmake)
conan_basic_setup()

# Add some options from https://sqlite.org/compile.html
option(ENABLE_JSON1 "Enable JSON SQL functions")
option(ENABLE_COLUMN_METADATA "Enable additional APIs that provide convenient access to meta-data about tables and queries")
option(ENABLE_EXPLAIN_COMMENTS "Enable SQLite to insert comment text into the output of EXPLAIN")
option(ENABLE_FTS3 "Enable version 3 of the full-text search engine")
option(ENABLE_FTS4 "Enable version 3 and 4 of the full-text search engine")
option(ENABLE_FTS5 "Enable version 5 of the full-text search engine")
option(ENABLE_RTREE "Enable support for the R*Tree index extension")
option(OMIT_LOAD_EXTENSION "Omits the entire extension loading mechanism from SQLite")
option(HAVE_FDATASYNC "Use fdatasync() instead of fsync() on unix systems")
option(HAVE_GMTIME_R "Use the threadsafe gmtime_r()")
option(HAVE_LOCALTIME_R "Use the threadsafe localtime_r()")
option(HAVE_POSIX_FALLOCATE "Use posix_fallocate()")
option(HAVE_STRERROR_R "Use strerror_r()")
option(HAVE_USLEEP "Use usleep() system call to implement the xSleep method")

add_executable(${PROJECT_NAME} source_subfolder/shell.c
                            source_subfolder/sqlite3.c
                            source_subfolder/sqlite3.h
                            source_subfolder/sqlite3ext.h)

if (UNIX)
    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_package(Threads REQUIRED)

    target_link_libraries(${PROJECT_NAME}
        PRIVATE Threads::Threads
        PRIVATE ${CMAKE_DL_LIBS}
    )
endif(UNIX)

if(ENABLE_JSON1)
    target_compile_definitions(${PROJECT_NAME} PRIVATE SQLITE_ENABLE_JSON1)
endif()
if(ENABLE_COLUMN_METADATA)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_COLUMN_METADATA)
endif()
if(ENABLE_EXPLAIN_COMMENTS)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_EXPLAIN_COMMENTS)
endif()
if(ENABLE_FTS3)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_FTS3)
endif()
if(ENABLE_FTS4)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_FTS4)
endif()
if(ENABLE_FTS5)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_FTS5)
endif()
if(ENABLE_RTREE)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_ENABLE_RTREE)
endif()
if(OMIT_LOAD_EXTENSION)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_OMIT_LOAD_EXTENSION)
endif()
if(HAVE_FDATASYNC)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_FDATASYNC)
endif()
if(HAVE_GMTIME_R)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_GMTIME_R)
endif()
if(HAVE_LOCALTIME_R)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_LOCALTIME_R)
endif()
if(HAVE_POSIX_FALLOCATE)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_POSIX_FALLOCATE)
endif()
if(HAVE_STRERROR_R)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_STRERROR_R)
endif()
if(HAVE_USLEEP)
    target_compile_definitions(${PROJECT_NAME}  PRIVATE HAVE_USLEEP)
endif()
target_compile_definitions(${PROJECT_NAME}  PRIVATE SQLITE_THREADSAFE=${THREADSAFE})

install(TARGETS ${PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(DIRECTORY source_subfolder/ DESTINATION include
        FILES_MATCHING PATTERN "*.h")
