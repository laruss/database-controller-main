# MongoDB Models Manager

This Python project is designed for local development with the possibility of connecting to a remote MongoDB database. It provides an easy way to manage MongoDB models and create RESTful endpoints using Flask, MongoEngine, and a BaseController. The project also utilizes a `.env` file for database configuration and includes a `main.py` file as the entry point.

## Features

- Flask server for creating RESTful API endpoints
- MongoEngine for defining MongoDB models
- BaseController for inheriting controller functionality
- Configuration via .env file
- Local development with the option to connect to a remote MongoDB database

## Installation

1. Clone this repository:
    
    ```bash
    git clone https://github.com/laruss/databaseControllerBack.git
    ```
   
2. Navigate to the project directory:
        
        ```bash
        cd databaseControllerBack
        ```
3. Install the dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
   
4. Create a `.env` file in the root directory and add the following variables:
    
    ```bash
    MONGODB_HOST=localhost
    MONGODB_PORT=27017
    MONGODB_DB=database_name
    MONGODB_USERNAME=username
    MONGODB_PASSWORD=password
    ```
   
5. Run the project:
    
    ```bash
    python main.py
    ```
   
6. Access the RESTful API endpoints via the browser, Postman, or other tools.
