# training-secure-transaction-processor
This project provides a collection of Python scripts demonstrating various aspects of application development, including secure transaction processing, external API integration with retry mechanisms, command-line data export utilities, and core order processing logic with comprehensive configuration management.

---
## Recent Changes
- Migrated from Basic Auth to JWT (Security upgrade).
- Updated API examples.

---

## 1. Table of Contents
*   [2. About The Project](#2-about-the-project)
*   [3. Installation](#3-installation)
*   [4. Usage](#4-usage)
*   [5. Configuration](#5-configuration)
*   [6. API Reference](#6-api-reference)
*   [7. Deployment](#7-deployment)
*   [8. Roadmap](#8-roadmap)
*   [9. License](#9-license)

## 2. About The Project
This repository contains Python scripts designed to illustrate core principles across different application domains:
*   **Secure Transaction Processing**: Demonstrates handling sensitive configuration and ensuring data integrity through hashing, similar to secure vault interactions.
*   **Vendor API Client**: `api_client.py` provides a robust client for interacting with external supplier APIs, featuring automatic retry logic (using `tenacity`) for network resilience and JWT-based authentication.
*   **Data Export Tool**: `export_tool.py` is a command-line interface (CLI) tool (built with `click`) to export data records to local files in various formats (CSV, JSON), with configurable output directory and row limits.
*   **Order Processing Engine**: The core `OrderProcessor` (found in `test file 2`) handles e-commerce order workflows, including inventory validation, payment calculation, and simulated payment capture. It also integrates fraud checks and leverages external inventory microservices.
*   **Environment Variable Usage**: Shows how to load sensitive and configurable information from environment variables, promoting secure and flexible deployment.

## 3. Installation
The project requires Python 3.x.
1.  Clone the repository:
    ```bash
    git clone https://github.com/your-org/training-secure-transaction-processor.git
    cd training-secure-transaction-processor
    
2.  Install the required Python packages:
    ```bash
    pip install requests tenacity click
    
    *   `requests`: For HTTP requests to external APIs.
    *   `tenacity`: For retry logic in API calls.
    *   `click`: For building command-line interfaces.

## 4. Usage
To run the original secure transaction processing script:
bash
python 123

This will execute the example call to `process_secure_transaction` with predefined `user_id` and `amount`. The output will show the processing message and the generated transaction signature.

To use the data export tool:
bash
python export_tool.py --format json --filename my_report

This will export dummy data to `exports/my_report.json`. You can specify `--format csv` for CSV output.

To demonstrate the `VendorApiClient` (requires `VENDOR_API_TOKEN` to be set):
python
# Example in your application code
from api_client import VendorApiClient

client = VendorApiClient()
if client.check_availability("SKU001"):
    print("Product SKU001 is available.")
else:
    print("Product SKU001 is out of stock or API call failed.")


To use the `OrderProcessor`:
python
# Example in your application code (from test file 2)
from test_file_2 import OrderProcessor # Assuming 'test file 2' is named for import

processor = OrderProcessor()
order = {"id": "ORD001", "item_id": "PROD123", "price": 100.00, "qty": 2, "amount": 200.00}
result = processor.process_order(order)
print(f"Order {result.order_id} status: {result.status}. Message: {result.message}")


## 5. Configuration
The scripts rely on several sensitive and configurable variables. **It is highly recommended to manage these securely, preferably through environment variables or a dedicated secret management system, and avoid hardcoding them directly in production environments.**

### General Configuration
*   `DB_CONNECTION_STRING` (or `DB_URL`): The database connection string. This is loaded from the `DB_URL` environment variable if set. Used in secure transaction processing and critical for the Order Processor.
*   `API_KEY_V1`: Your API key for interacting with external services (used in original secure transaction processor).
*   `ADMIN_PASSWORD`: An administrative password used as part of the transaction signature generation.

### Vendor API Client (`api_client.py`)
*   `VENDOR_API_URL`: Base URL for the external supplier API (default: `https://api.supplier.com/v1`).
*   `VENDOR_API_TOKEN`: **Required** JWT token for authenticating with the vendor API.
*   `REQUEST_TIMEOUT`: Timeout for API requests in seconds (default: `30`).

### Data Export Tool (`export_tool.py`)
*   `EXPORT_DIR`: Default directory where exported files will be saved (default: `./exports`).
*   `MAX_EXPORT_ROWS`: Maximum number of rows to export (default: `1000`).

### Order Processing Engine (`test file 2`)
*   `APP_ENV`: Application environment (default: `development`).
*   `PAYMENT_GATEWAY_KEY` (or `STRIPE_SECRET_KEY`): **Required** secret key for the payment gateway (e.g., Stripe).
*   `INVENTORY_SERVICE_URL`: URL for the external inventory microservice (default: `http://inventory-service:8080`).
*   `TAX_RATE`: Default tax rate as a float (default: `0.20`).
*   `ENABLE_FRAUD_CHECK`: Boolean flag to enable/disable fraud checks (default: `True`).

**Example for setting environment variables (before running the scripts):**
bash
export DB_URL="postgres://user:secret@your_db_host:5432/production_db"
export API_KEY_V1="sk_live_YOUR_ACTUAL_API_KEY"
export ADMIN_PASSWORD="your-strong-admin-password"
export VENDOR_API_URL="https://api.myvendors.com/v2"
export VENDOR_API_TOKEN="your_jwt_vendor_token_here"
export STRIPE_SECRET_KEY="sk_live_YOUR_STRIPE_SECRET_KEY"
export INVENTORY_URL="http://prod-inventory:8080"
export MAX_EXPORT_ROWS="5000"

python 123
python export_tool.py --format csv


## 6. API Reference

### `process_secure_transaction(user_id, amount)` (Original Secure Transaction Processor)
Encrypts transaction data and sends it to a secure vault (simulated).

**Args:**
*   `user_id` (`str`): The unique identifier for the user involved in the transaction.
*   `amount` (`float`): The monetary amount of the transaction.

**Returns:**
*   `dict`: A dictionary indicating the status of the transaction and a transaction ID (which is the generated signature in this example).
    *   Example: `{"status": "success", "tx_id": "..."}`

**Raises:**
*   `ValueError`: If `API_KEY_V1` is not configured (e.g., is an empty string).

### `class VendorApiClient` (`api_client.py`)
Client for interacting with external supplier APIs, includes automatic retry logic.

#### `VendorApiClient.check_availability(sku: str) -> bool`
Checks if a product is available at the supplier. Retries 3 times if the connection fails.

**Args:**
*   `sku` (`str`): The product Stock Keeping Unit.

**Returns:**
*   `bool`: `True` if the product is in stock, `False` otherwise or if the API call fails.

**Raises:**
*   `requests.RequestException`: If the API request fails after all retries.

### `export_data` (CLI Command from `export_tool.py`)
CLI Tool to export database records to local files.

**Usage:**
bash
python export_tool.py --format [csv|json] --filename [output_filename]


**Options:**
*   `--format {csv,json}`: Output format for the export. Default is `csv`.
*   `--filename TEXT`: Output filename without extension. Default is `data_export`.

### `class OrderProcessor` (Core Order Processing Engine from `test file 2`)
Core logic for handling e-commerce orders, performing validation, inventory reservation, and payment capture.

**Raises:**
*   `ValueError`: If `PAYMENT_GATEWAY_KEY` is not set during initialization.

#### `OrderProcessor.validate_stock(item_id: str, quantity: int) -> bool`
Checks inventory availability via an external microservice defined by `INVENTORY_SERVICE_URL`.

**Args:**
*   `item_id` (`str`): The identifier for the item.
*   `quantity` (`int`): The desired quantity.

**Returns:**
*   `bool`: `True` if sufficient stock is available, `False` otherwise.

#### `OrderProcessor.calculate_total(price: float) -> float`
Applies tax rates based on the `TAX_RATE_DEFAULT` environment configuration.

**Args:**
*   `price` (`float`): The base price of the item(s).

**Returns:**
*   `float`: The total price after applying tax.

#### `OrderProcessor.process_order(order_payload: Dict) -> OrderResult`
Main entry point for processing a single order. Performs fraud checks, inventory validation, and simulates payment capture.

**Args:**
*   `order_payload` (`dict`): JSON containing order details, expected keys include `id`, `item_id`, `price`, `qty`, `amount`.

**Returns:**
*   `OrderResult`: A dataclass containing `order_id`, `status`, `total_charged`, and a `message` describing the outcome.

## 7. Deployment
When deploying these components in a production environment, consider the following best practices for security and reliability:
*   **Environment Variables & Secret Management**: Always use environment variables or a secure secret management system (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) for sensitive credentials like `API_KEY_V1`, `VENDOR_API_TOKEN`, `PAYMENT_GATEWAY_KEY`.
*   **Least Privilege**: Ensure that the execution environment and the scripts themselves have only the minimum necessary permissions required to perform their functions.
*   **Secure Communications**: Use TLS/SSL for all communication channels, especially when transmitting sensitive data to payment gateways or external APIs.
*   **Logging & Auditing**: Implement robust logging for transactions, security events, and API interactions. Regularly audit access and transactions for suspicious activity.
*   **Microservice Reliability**: For services interacting with external microservices (e.g., Inventory Service), consider circuit breakers, health checks, and advanced retry strategies in addition to basic retries.
*   **Error Handling**: Implement comprehensive error handling and fallback mechanisms for API failures and other exceptional conditions.

## 8. Roadmap
*   Implement actual cryptographic encryption for transaction data before transmission.
*   Integrate with a real secure vault service or API.
*   Add more comprehensive error handling and detailed logging for various transaction states.
*   Introduce unit and integration tests to ensure reliability and security.
*   Explore asynchronous processing for high-volume transactions.
*   Expand `VendorApiClient` to support more vendor endpoints (e.g., order placement, shipping status).
*   Enhance `export_tool` with database integration for exporting real data and support for more complex queries.
*   Integrate `OrderProcessor` with a real payment gateway (e.g., Stripe SDK) and a persistent database.
*   Add more sophisticated fraud detection mechanisms in the `OrderProcessor`.

## 9. License
Copyright © 2024 Grid Dynamics Holdings, Inc. All rights reserved.

This software and associated documentation files (the "Software")
are the confidential and proprietary information of Grid Dynamics
Holdings, Inc. and may not be copied, reproduced, modified, published,
uploaded, posted, transmitted, or distributed in any form or by any
means without prior written permission.

For questions regarding licensing or usage,
contact legal_operations@griddynamics.com

