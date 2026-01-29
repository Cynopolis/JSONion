cmake_minimum_required(VERSION 3.10)

project(generated_commands LANGUAGES CXX)

# ------------------------------------------------------------
# Header-only interface library
# ------------------------------------------------------------
add_library(generated-commands-intf
    INTERFACE
)

# Expose this directory as an include path
target_include_directories(generated-commands-intf
    INTERFACE
        ${CMAKE_CURRENT_LIST_DIR}
)

# Require C++17
target_compile_features(generated-commands-intf
    INTERFACE
        cxx_std_17
)

# Optional: only include this if you want to enforce JSON
# target_link_libraries(generated-commands-intf
#     INTERFACE
#         nlohmann_json::nlohmann_json
# )
