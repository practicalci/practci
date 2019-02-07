cmake_minimum_required(VERSION 3.5)

project(dummy_cpp)

# invoke cmake with -DCMAKE_INSTALL_PREFIX=<install_dir>

include(GNUInstallDirs)

add_executable(dummy_cpp main.cpp)

install(TARGETS dummy_cpp DESTINATION ${CMAKE_INSTALL_BINDIR})
