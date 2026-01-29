// Auto-generated file. Do not edit manually.
#pragma once

#include <string>
#include <optional>

namespace GeneratedCommands
{
    /**
     * @brief This is a test command.
     */
    class ExampleCommand : public Command
    {
    public:
        /**
         * @brief Example message
         */
        std::string SomeMessage;
        /**
         * @brief Example count
         */
        int Count;
        /**
         * @brief Example bool
         */
        bool SomeBooleanExample;
        /**
         * @brief Optional string
         */
        std::optional<std::string> CouldBeNothing;
    };

    /**
     * @brief This command just shows another example.
     */
    class AnotherExampleCommand : public Command
    {
    public:
        // No fields defined
    };

}