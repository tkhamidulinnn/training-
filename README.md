**PART 2: FULL README**
# training-secure-transaction-processor

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-33CC33?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

This project provides a collection of Python scripts demonstrating secure transaction processing, asynchronous task management with Celery, system health monitoring, and external API integration for weather data. It focuses on handling sensitive configuration and data integrity through hashing.

## 📂 Project Structure

.
├── Dockerfile
├── README.md
├── health_monitor.py
├── new # Celery tasks module (interpreted as new.py)
└── weather_api.py


## 1. Table of Contents
*   [2. About The Project](#2-about-the-project)
*   [3. Installation](#3-installation)
    *   [3.1. Dependencies](#31-dependencies)
    *   [3.2. Docker Containerization](#32-docker-containerization)
*   [4. Usage](#4-usage)
*   [5. Configuration](#5-configuration)
*   [6. API Reference](#6-api-reference)
*   [7. Deployment](#7-deployment)
*   [8. Roadmap](#8-roadmap)
*   [9. License](#9-license)

## 2. About The Project
This repository contains Python scripts designed to illustrate basic principles of secure transaction processing, asynchronous task management, system monitoring, and external API integration. It includes:
*   **Security Configuration**: Demonstrates how sensitive credentials like API keys and administrative passwords might be handled in code, emphasizing the need for secure management.
*   **Data Hashing**: Utilizes SHA256 for creating a transaction signature to ensure data integrity before transmission to a simulated secure vault.
*   **Transaction Processing**: A function `process_secure_transaction` that simulates the encryption and sending of data.
*   **Environment Variable Usage**: Shows how to load sensitive information from environment variables, with a fallback to default values.
*   **Asynchronous Tasks**: An example (`new`) demonstrating background task processing using Celery and Redis, including email sending and report generation.
*   **System Health Monitoring**: A script (`health_monitor.py`) to continuously monitor CPU and memory usage, with configurable thresholds and webhook alerts for critical conditions.
*   **External API Integration (Weather)**: A module (`weather_api.py`) for fetching current weather data from the OpenWeatherMap API, demonstrating integration with external services.

## 3. Installation
The project requires Python 3.x.

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-org/training-secure-transaction-processor.git
    cd training-secure-transaction-processor
    
2.  Install the required Python packages:
    ```bash
    pip install requests celery redis psutil
    
3.  Ensure a Redis server is running, as it's used by Celery for brokering tasks and storing results. You can typically run Redis via Docker or directly install it on your system.

### 3.1. Dependencies

This project relies on the following external libraries:

| Dependency | Version | Description |
| :--------- | :------ | :---------- |
| `requests` | Any     | Used for making HTTP requests (e.g., to external services, webhooks, OpenWeatherMap). |
| `celery`   | Any     | Asynchronous task queue/job queue for background processing. |
| `redis`    | Any     | In-memory data structure store, used as Celery's message broker and result backend. |
| `psutil`   | Any     | Cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network). |
| `pandas`   | Any     | (Referenced in Dockerfile) Data analysis and manipulation tool. |
| `sqlalchemy` | Any     | (Referenced in Dockerfile) SQL toolkit and Object-Relational Mapper. |
| `psycopg2-binary` | Any | (Referenced in Dockerfile) PostgreSQL database adapter for Python. |

### 3.2. Docker Containerization
A `Dockerfile` is provided for containerizing a related application component.
To build the Docker image:
bash
docker build -t training-processor-app .

To run the container (note: this will run `order_processor.py` as defined in the `Dockerfile`):
bash
docker run -p 80:80 -e APP_ENV=production training-processor-app

*Note: The `Dockerfile` specifically targets `order_processor.py` and includes additional dependencies (`pandas`, `sqlalchemy`, `psycopg2-binary`) which are not explicitly part of the primary `process_secure_transaction`, Celery task, health monitor, or weather API examples detailed in this README.*

## 4. Usage
To run the secure transaction script (assuming `123` is a Python script, e.g., `123.py`):
bash
python 123

This will execute the example call to `process_secure_transaction` with predefined `user_id` and `amount`. The output will show the processing message and the generated transaction signature.

To use the Celery example (assuming the file `new` is `new.py`):

1.  Start a Celery worker in a dedicated terminal:
    ```bash
    celery -A new worker --loglevel=info
    
    (Note: If `new` is not directly importable as a Python module, you might need to adjust the command, e.g., `celery -A your_app_name worker --loglevel=info` if `new.py` defines the app.)

2.  In a separate Python interpreter or script, trigger tasks:
    ```python
    from new import send_welcome_email, generate_monthly_report
    
    # Send a welcome email asynchronously
    email_task = send_welcome_email.delay(user_id=123, email="user@example.com")
    print(f"Welcome email task ID: {email_task.id}")
    
    # Generate a monthly report
    report_task = generate_monthly_report.delay(month="August")
    print(f"Report generation task ID: {report_task.id}")
    
    # You can check the status and result later (e.g., in a web app)
    # print(email_task.status)
    # print(email_task.result)
    

To run the System Health Monitor:
bash
python health_monitor.py

This will perform a single health check. For continuous monitoring, you might run it in a loop or schedule it:
bash
# Example for continuous monitoring (run in background with nohup or a service manager)
# MONITOR_INTERVAL=30 # check every 30 seconds
# while true; do python health_monitor.py; sleep $MONITOR_INTERVAL; done


To use the Weather API:
python
# In a Python script or interpreter
from weather_api import WeatherAPI

weather_api = WeatherAPI()
city = "London"
weather_data = weather_api.get_current_weather(city)

if weather_data:
    print(f"Current weather in {city}:")
    print(f"Temperature: {weather_data['main']['temp']} Kelvin") # OpenWeatherMap defaults to Kelvin
    print(f"Description: {weather_data['weather'][0]['description']}")
else:
    print(f"Could not retrieve weather for {city}.")


## 5. Configuration
The scripts rely on several configuration variables, some of which are sensitive. **It is highly recommended to manage these securely, preferably through environment variables or a dedicated secret management system, and avoid hardcoding them directly in production environments.**

| Variable                | Description                                                                                             | Environment Variable      | Default Value                      |
| :---------------------- | :------------------------------------------------------------------------------------------------------ | :------------------------ | :--------------------------------- |
| `API_KEY_V1`            | Your API key for interacting with external services (e.g., transaction vault).                          | `API_KEY_V1`              | `sk_live_YOUR_ACTUAL_API_KEY`      |
| `ADMIN_PASSWORD`        | An administrative password used as part of the transaction signature generation.                        | `ADMIN_PASSWORD`          | `your-strong-admin-password`       |
| `DB_CONNECTION_STRING`  | The database connection string.                                                                         | `DB_URL`                  | `postgres://user:secret@your_db_host:5432/production_db` |
| `CELERY_BROKER_URL`     | URL for the Celery message broker (e.g., Redis, RabbitMQ).                                              | `CELERY_BROKER_URL`       | `redis://localhost:6379/0`         |
| `CELERY_RESULT_BACKEND` | URL for the Celery result backend to store task results.                                                | `CELERY_RESULT_BACKEND`   | `redis://localhost:6379/0`         |
| `EMAIL_SENDER`          | Default sender email address for system notifications in the Celery email task.                         | `MAIL_DEFAULT_SENDER`     | `noreply@example.com`              |
| `MONITOR_INTERVAL`      | Interval in seconds for the health monitor to run checks.                                               | `MONITOR_INTERVAL`        | `60`                               |
| `ALERT_WEBHOOK_URL`     | Webhook URL for sending system alerts (e.g., Slack, Teams). If not set, alerts are printed to console.  | `ALERT_WEBHOOK_URL`       | `None`                             |
| `CPU_THRESHOLD`         | CPU usage percentage threshold (0-100) for critical alert.                                              | `CPU_THRESHOLD`           | `85.0`                             |
| `MEMORY_THRESHOLD`      | Memory usage percentage threshold (0-100) for critical alert.                                           | `MEMORY_THRESHOLD`        | `90.0`                             |
| `OPENWEATHER_API_KEY`   | API key for accessing the OpenWeatherMap service.                                                       | `OPENWEATHER_API_KEY`     | `YOUR_OPENWEATHER_API_KEY`         |
| `OPENWEATHER_BASE_URL`  | Base URL for the OpenWeatherMap API.                                                                    | `OPENWEATHER_BASE_URL`    | `http://api.openweathermap.org/data/2.5/weather` |

**Example for setting environment variables (before running the script or starting the Celery worker):**
bash
export DB_URL="postgres://user:secret@your_db_host:5432/production_db"
export API_KEY_V1="sk_live_YOUR_ACTUAL_API_KEY"
export ADMIN_PASSWORD="your-strong-admin-password"
export CELERY_BROKER_URL="redis://your_redis_host:6379/0"
export CELERY_RESULT_BACKEND="redis://your_redis_host:6379/0"
export MAIL_DEFAULT_SENDER="admin@yourdomain.com"
export MONITOR_INTERVAL="30"
export ALERT_WEBHOOK_URL="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
export CPU_THRESHOLD="90.0"
export MEMORY_THRESHOLD="95.0"
export OPENWEATHER_API_KEY="your_actual_openweathermap_api_key"
export OPENWEATHER_BASE_URL="http://api.openweathermap.org/data/2.5/weather"

# Then run your script or start your Celery worker
# python 123
# celery -A new worker --loglevel=info
# python health_monitor.py
# python -c "from weather_api import WeatherAPI; api=WeatherAPI(); print(api.get_current_weather('London'))"


## 6. API Reference
### `process_secure_transaction(user_id, amount)`

Encrypts transaction data and sends it to a secure vault (simulated).

**Args:**
*   `user_id` (`str`): The unique identifier for the user involved in the transaction.
*   `amount` (`float`): The monetary amount of the transaction.

**Returns:**
*   `dict`: A dictionary indicating the status of the transaction and a transaction ID (which is the generated signature in this example).
    *   Example: `{"status": "success", "tx_id": "..."}`

**Raises:**
*   `ValueError`: If `API_KEY_V1` is not configured (e.g., is an empty string).

---

### `send_welcome_email(user_id, email)` (Celery Task)

Background task to send onboarding emails to new users. Retries automatically on failure.

**Args:**
*   `user_id` (`int`): The user's database ID.
*   `email` (`str`): Recipient email address.

**Returns:**
*   `dict`: A dictionary indicating the status and recipient upon successful processing.
    *   Example: `{"status": "sent", "recipient": "user@example.com"}`

---

### `generate_monthly_report(month)` (Celery Task)

Heavy task that simulates the generation of a PDF report for a given month.

**Args:**
*   `month` (`str`): The specific month for which the report is to be generated (e.g., "August").

**Returns:**
*   `str`: The path to the generated report file.
    *   Example: `"/tmp/report_August.pdf"`

---

### `SystemMonitor.run_check()`

Performs a one-time system health check for CPU and memory usage. If configured, sends an alert via a webhook URL if usage exceeds defined thresholds. Prints a report to the console.

**Args:** None

**Returns:** None (prints report to console, sends webhook alert if configured and thresholds are met).

---

### `WeatherAPI.get_current_weather(city)`

Fetches current weather data for a specified city from the OpenWeatherMap API.

**Args:**
*   `city` (`str`): The name of the city to get weather for.

**Returns:**
*   `dict` or `None`: A dictionary containing weather data if the request is successful, `None` otherwise (e.g., API key missing, city not found, network error).
    *   Example (partial): `{"coord": {"lon": -0.13, "lat": 51.51}, "weather": [{"id": 800, "main": "Clear", "description": "clear sky", ...}], "main": {"temp": 285.32, "feels_like": 284.14, ...}}`

**Raises:**
*   `ValueError`: If `OPENWEATHER_API_KEY` is not configured in the environment.
*   `requests.exceptions.RequestException`: For network-related issues during the API call.

## 7. Deployment
When deploying this project or similar components in a production environment, consider the following best practices for security and reliability:
*   **Environment Variables & Secret Management**: Always use environment variables or a secure secret management system (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) for sensitive credentials instead of hardcoding. This includes `API_KEY_V1`, `ADMIN_PASSWORD`, `DB_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `ALERT_WEBHOOK_URL`, and `OPENWEATHER_API_KEY`.
*   **Containerization**: Consider deploying applications within Docker containers for isolation, portability, and consistent environments. The provided `Dockerfile` offers a starting point for containerizing a component of this project.
*   **Orchestration**: For scalable deployments, use container orchestration platforms like Kubernetes or Docker Swarm, especially for managing Celery workers and Redis instances.
*   **Dedicated Processes**: For the `health_monitor.py` script, consider running it as a scheduled cron job (e.g., via `cron` or a Kubernetes `CronJob`) or as a dedicated background process/sidecar. Ensure `ALERT_WEBHOOK_URL` and thresholds are securely configured.
*   **Least Privilege**: Ensure that the execution environment and the script itself have only the minimum necessary permissions required to perform their functions.
*   **Secure Communications**: Use TLS/SSL for all communication channels, especially when transmitting sensitive data (e.g., between application and Redis, to external APIs like OpenWeatherMap, or to webhook endpoints).
*   **Logging & Auditing**: Implement robust logging for transactions, task processing, health checks, and security events. Regularly audit access and transactions for suspicious activity.
*   **Monitoring**: Set up monitoring for Celery workers, Redis, and application performance to detect and address issues proactively. This can be complemented by the `health_monitor.py` script for basic system resource checks.

## 8. Roadmap
*   Implement actual cryptographic encryption for transaction data before transmission.
*   Integrate with a real secure vault service or API.
*   Add more comprehensive error handling and detailed logging for various transaction states and Celery task failures.
*   Introduce unit and integration tests to ensure reliability and security.
*   Explore asynchronous processing for high-volume transactions beyond the basic Celery example.
*   Implement a proper `requirements.txt` file for easier dependency management.
*   Integrate health monitoring into a dashboard or more sophisticated alerting system (e.g., Prometheus/Grafana).
*   Extend `weather_api.py` to fetch forecasts or historical data.
*   Consider adding more system metrics to `health_monitor.py` (e.g., disk I/O, network usage).

## 9. License
Copyright © 2025 Grid Dynamics Holdings, Inc. All rights reserved.

This software and associated documentation files (the "Software")
are the confidential and proprietary information of Grid Dynamics
Holdings, Inc. and may not be copied, reproduced, modified, published,
uploaded, posted, transmitted, or distributed in any form or by any
means without prior written permission.

Unauthorized use, reproduction, or distribution of the Software or any
portion of it may result in civil and criminal penalties.

For questions regarding licensing or usage,
contact legal_operations@griddynamics.com