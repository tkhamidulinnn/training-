/**
 * Simple Logger Utility
 * Helps to track application events.
 */
class Logger {
    constructor(prefix) {
        this.prefix = prefix || 'APP';
    }

    log(message) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [${this.prefix}]: ${message}`);
    }

    error(message) {
        console.error(`ERROR: ${message}`);
    }
}

module.exports = Logger;
