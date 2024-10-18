<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
AI Powered Request Handler Tool
</h1>
<h4 align="center">A Python backend service that simplifies user interaction with OpenAI's API</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="Language: Python" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-red" alt="Framework: FastAPI" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="Database: PostgreSQL" />
  <img src="https://img.shields.io/badge/API-OpenAI-black" alt="API: OpenAI" />
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/AI-Powered-Request-Handler-Tool?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/AI-Powered-Request-Handler-Tool?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/AI-Powered-Request-Handler-Tool?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview

This repository contains the backend code for the AI Powered Request Handler Tool, a Python service designed to act as a user-friendly intermediary between developers and OpenAI's API. It simplifies complex AI interactions, making advanced language processing accessible to a wider audience. This MVP addresses the growing need for user-friendly AI integration, empowering developers and users alike with a powerful, yet intuitive interface for leveraging OpenAI's capabilities. 

The tool's core value proposition lies in its ability to streamline the process of sending requests to OpenAI's API and receiving processed responses. This eliminates the complexities of direct API interactions and allows users to focus on the core functionalities of their applications.

## 📦 Features

|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The MVP utilizes a serverless architecture with a Python backend deployed on a cloud platform (e.g., AWS Lambda, Azure Functions) triggered by user requests through either a command-line interface or API calls. |
| 📄 | **Documentation**  | This README file provides a comprehensive overview of the MVP, its dependencies, and usage instructions.|
| 🔗 | **Dependencies**   | The codebase relies on various external libraries and packages such as `FastAPI`, `uvicorn`, `pydantic`, `psycopg2-binary`, `python-dotenv`, `openai`, `sqlalchemy`, `requests`, `pytest`, `docker`, `docker-compose`, `prometheus_client`, `gunicorn`, and `sentry-sdk`.|
| 🧩 | **Modularity**     | The code is organized into modules for different functionalities (e.g., routers, models, schemas, services, utils, tests), promoting reusability and maintainability.|
| 🧪 | **Testing**        | Unit tests are included for key modules like `openai_service` and `db_service` to ensure functionality and correctness.|
| ⚡️  | **Performance**    |  The backend is optimized for efficient request processing and response handling, including techniques like caching frequently used API calls and minimizing unnecessary API requests.|
| 🔐 | **Security**       |  Robust authentication and authorization measures are implemented to protect API keys and user data. Secure communication protocols (HTTPS) are used for all API interactions. |
| 🔀 | **Version Control**| Utilizes Git for version control with a `startup.sh` script for containerized deployment. |
| 🔌 | **Integrations**   |  The MVP seamlessly integrates with OpenAI's API, PostgreSQL database, and utilizes various Python libraries for HTTP requests, JSON handling, and logging. |
| 📶 | **Scalability**    |  The architecture is designed to handle increasing user load and evolving OpenAI API features. Considerations for load balancing, horizontal scaling, and efficient database management are implemented.|

## 📂 Structure

```text
├── main.py             # Main application entry point
├── routers
│   ├── requests.py     # API endpoint for handling user requests
│   └── settings.py    # API endpoint for managing user settings
├── models
│   ├── request.py      # Database model for user requests
│   └── settings.py     # Database model for user settings
├── schemas
│   ├── request_schema.py # Pydantic schema for validating user requests
│   └── settings_schema.py # Pydantic schema for validating user settings
├── services
│   ├── openai_service.py # Service for interacting with the OpenAI API
│   └── db_service.py    # Service for interacting with the database
├── utils
│   ├── logger.py       # Logging utility for the application
│   ├── exceptions.py    # Custom exception classes for error handling
│   └── config.py       # Configuration utility for loading environment variables
└── tests
    └── unit
        ├── test_openai_service.py # Unit tests for the openai_service module
        └── test_db_service.py     # Unit tests for the db_service module
```

## 💻 Installation

### 🔧 Prerequisites
- Python 3.9+
- PostgreSQL 15+
- Docker 5.0.0+

### 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/coslynx/AI-Powered-Request-Handler-Tool.git
   cd AI-Powered-Request-Handler-Tool
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add the following environment variables:
     ```
     OPENAI_API_KEY=YOUR_API_KEY
     DATABASE_URL=postgresql://user:password@host:port/database
     ```

4. Start the database (if necessary):
   ```bash
   docker-compose up -d db
   ```

## 🏗️ Usage

### 🏃‍♂️ Running the MVP

1. Start the application:
   ```bash
   docker-compose up
   ```

2. Access the application:
   - API endpoint: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🌐 Hosting

### 🚀 Deployment Instructions

1. Build the Docker image:
   ```bash
   docker build -t ai-request-handler .
   ```

2. Deploy the container to a cloud platform (e.g., AWS ECS, Google Kubernetes Engine):
   - Configure the cloud platform with necessary resources (e.g., database, load balancer).
   - Create a deployment configuration for the `ai-request-handler` image.

3. Configure environment variables (similar to the `.env` file) on the cloud platform.

4. Deploy the application.

### 🔑 Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.
- `DATABASE_URL`:  The connection string to your PostgreSQL database.

## 📜 API Documentation

### 🔍 Endpoints

- **POST `/requests`:** Sends a request to the OpenAI API.
  - **Request Body:**
    ```json
    {
      "prompt": "Write a short story about a dog and a cat",
      "model": "text-davinci-003",
      "temperature": 0.7
    }
    ```
  - **Response Body:**
    ```json
    {
      "status": "success",
      "response": "Once upon a time, there was a dog named..." 
    }
    ```

- **GET `/settings`:** Retrieves user settings.
  - **Response Body:**
    ```json
    {
      "api_key": "YOUR_API_KEY",
      "preferred_model": "text-davinci-003" 
    }
    ```

- **PUT `/settings`:** Updates user settings.
  - **Request Body:**
    ```json
    {
      "api_key": "NEW_API_KEY",
      "preferred_model": "text-curie-001" 
    }
    ```

## 📜 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: AI-Powered-Request-Handler-Tool

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
  <img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
  <img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
  <img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>