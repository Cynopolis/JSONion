/**
 * Base class for all generated commands.
 * Provides:
 * - automatic JSON serialization/deserialization
 * - a commandName property in snake_case
 */
export class Command {
    constructor() {
        this.commandName = this.constructor.name
            .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
            .replace(/([A-Z]+)([A-Z][a-z])/g, '$1_$2')
            .toLowerCase();
    }

    /**
     * Serialize this command to a JSON string
     */
    toJson() {
        return JSON.stringify(this, null, 4);
    }

    /**
     * Deserialize a JSON string to an instance of the given class
     * @param {string} json 
     * @param {Function} cls - The class to instantiate
     */
    static fromJson(json, cls) {
        const obj = JSON.parse(json);
        const instance = new cls();
        Object.assign(instance, obj);
        return instance;
    }
}
