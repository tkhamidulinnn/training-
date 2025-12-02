**PART 1: CHANGE LOG**
*   :sparkles: **New Feature**: Introduced `api_client.py` for robust external supplier API integration with JWT authentication and automatic retry logic (using `tenacity`).
*   :sparkles: **New Feature**: Added `export_tool.py`, a `click`-based command-line interface (CLI) tool for exporting data records to local files in various formats (CSV, JSON).
*   :sparkles: **New Feature**: Implemented `test file 2` which contains the `OrderProcessor` for comprehensive e-commerce order processing, including inventory validation, payment calculation, simulated payment capture, and fraud checks.
*   :gear: **Integration**: Documented the existing `currency_service.py` module, which provides real-time currency conversion functionality.
*   :pencil: **Documentation Update**: Expanded the main project description and "About The Project" section to reflect the new application components.
*   :wrench: **Dependencies**: Updated "Installation" instructions to include new required Python packages (`tenacity`, `click`).
*   :rocket: **Usage Examples**: Significantly expanded the "Usage" section with detailed examples for running the new `export_tool.py`, interacting with `VendorApiClient`, utilizing `OrderProcessor`, and demonstrating `CurrencyConverter`.
*   :card_file_box: **Configuration**: Extended the "Configuration" section to include environment variables and settings for the Vendor API Client, Data Export Tool, Order Processing Engine, and Currency Converter.
*   :books: **API Reference**: Updated the "API Reference" section with detailed documentation for `VendorApiClient`, `CurrencyConverter`, `export_data` CLI command, and `OrderProcessor` class and its methods.
*   :cloud: **Deployment**: Enhanced the "Deployment" section with more comprehensive best practices tailored for multi-component systems and microservice interactions.
*   :scroll: **Roadmap**: Updated the "Roadmap" to include future development plans for the newly introduced features.
*   :date: **Legal**: Corrected the License copyright year from 2025 to 2024.