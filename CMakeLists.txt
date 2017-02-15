cmake_minimum_required(VERSION 3.5.0)

add_subdirectory(meta)

project(metac)

file(
  GLOB_RECURSE
  ${PROJECT_NAME}_SOURCES

  ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
)
file(
  GLOB_RECURSE
  ${PROJECT_NAME}_HEADERS

  ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp
  ${CMAKE_CURRENT_SOURCE_DIR}/include/*.inl
)

find_package(Boost 1.58 REQUIRED COMPONENTS system filesystem)

add_executable(
  ${PROJECT_NAME}
  ${${PROJECT_NAME}_SOURCES}
  ${${PROJECT_NAME}_HEADERS}
)

target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

target_link_libraries(${PROJECT_NAME} meta ${Boost_LIBRARIES})

set_target_properties(
  metac PROPERTIES
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
  ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib
)

set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 14)
