#pragma once

#include <nlohmann/json.hpp>
#include <optional>
#include <regex>
#include <string>
#include <typeinfo>

namespace GeneratedCommands {

/**
 * @brief Base class for all generated commands.
 *
 * Provides:
 * - automatic JSON serialization/deserialization
 * - a CommandName field in snake_case matching the class name
 */
class Command {
public:
  /**
   * @brief Name of the command in snake_case (matches class name)
   */
  std::string CommandName;

  /**
   * @brief Construct a command and initialize CommandName
   */
  Command()
      : CommandName(
            convert_to_snake_case(demangle_type_name(typeid(*this).name()))) {}

  virtual ~Command() = default;

  /**
   * @brief Serialize this command to a JSON object
   */
  virtual nlohmann::json to_json() const { return nlohmann::json(*this); }

  /**
   * @brief Serialize this command to a formatted JSON string
   */
  std::string to_json_string(int indent = 4) const {
    return to_json().dump(indent);
  }

  /**
   * @brief Deserialize a JSON string into a command of type T
   */
  template <typename T> static T from_json(const std::string &json) {
    return nlohmann::json::parse(json).get<T>();
  }

protected:
  /**
   * @brief Convert PascalCase to snake_case
   */
  static std::string convert_to_snake_case(const std::string &name) {
    std::string s1 =
        std::regex_replace(name, std::regex("(.)([A-Z][a-z]+)"), "$1_$2");
    std::string s2 =
        std::regex_replace(s1, std::regex("([a-z0-9])([A-Z])"), "$1_$2");

    std::string result;
    result.reserve(s2.size());
    for (char c : s2)
      result.push_back(static_cast<char>(std::tolower(c)));

    return result;
  }

  /**
   * @brief Strip compiler-specific type decorations
   *
   * Example:
   * - "class GeneratedCommands::ExampleCommand"
   * - "GeneratedCommands::ExampleCommand"
   */
  static std::string demangle_type_name(const std::string &raw) {
    std::string name = raw;

    // Remove common prefixes
    const std::string class_prefix = "class ";
    if (name.starts_with(class_prefix))
      name.erase(0, class_prefix.size());

    // Remove namespace
    auto pos = name.rfind("::");
    if (pos != std::string::npos)
      name = name.substr(pos + 2);

    return name;
  }
};

} // namespace GeneratedCommands
