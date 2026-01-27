using System;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

namespace GeneratedCommands
{
/// <summary>
/// Base class for all generated commands.
/// Provides:
/// - automatic JSON serialization/deserialization
/// - a CommandName field in snake_case matching the class name
/// </summary>
public abstract class Command
{
    /// <summary>
    /// Name of the command in snake_case (matches class name)
    /// </summary>
    public string CommandName { get; set; }

    protected Command()
    {
        CommandName = ConvertToSnakeCase(this.GetType().Name);
    }

    /// <summary>
    /// Convert the PascalCase class name to snake_case
    /// </summary>
    private string ConvertToSnakeCase(string name)
    {
        string s1 = Regex.Replace(name, "(.)([A-Z][a-z]+)", "$1_$2");
        string s2 = Regex.Replace(s1, "([a-z0-9])([A-Z])", "$1_$2");
        return s2.ToLower();
    }

    /// <summary>
    /// Serialize this command to a JSON string
    /// </summary>
    public string ToJson()
    {
        var options = new JsonSerializerOptions { WriteIndented = true,
                                                  DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull };
        return JsonSerializer.Serialize(this, options);
    }

    /// <summary>
    /// Deserialize a JSON string to a command of type T
    /// </summary>
    public static T FromJson<T>(string json)
        where T : Command
    {
        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        return JsonSerializer.Deserialize<T>(json, options);
    }
}
}
