# SQL Agent

This project is a powerful SQL agent built with **Vanna** that connects to a MySQL database, leverages OpenAI for intelligent processing, and provides easy-to-use tools for managing and interacting with your data.

## Features

- **SQL Querying**: Interact with your MySQL database directly through the agent.
- **Intelligent Response Generation**: Powered by OpenAI's GPT-4 model to process and respond to queries.
- **User Management**: Supports simple user authentication and role-based access.
- **Agent Memory**: Stores interactions and tools used for improved performance.
- **FastAPI Integration**: Exposes the agent as a FastAPI server for easy interaction.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.7+
- OpenAI API Key (for GPT-4 integration)
- MySQL Database
- Other Python dependencies listed in `requirements.txt`

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/sql-agent.git
   cd sql-agent


## Install dependencies:

Ensure you have pip installed, then run:
```
pip install -r requirements.txt
```
### Configure environment variables:

Create a .env file in the root directory of your project and add the following (replace values with your actual credentials):
```
OPENAI_API_KEY="Your OpenAI API Key"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_DB="Your Database Name"
MYSQL_USER="Your Database Username"
MYSQL_PASSWORD="Your Database Password"

```
### Run the application:

To start the agent server, simply run the following:
```
python app.py
```

The agent will now be running on http://localhost:8000.