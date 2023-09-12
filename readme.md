# MongoDB Models Manager

This Python project is designed for local development with the possibility of connecting to a remote MongoDB database. 
It provides an easy way to manage MongoDB models and create RESTful endpoints using 
[Flask](https://flask.palletsprojects.com/),
[pydantic-mongo](https://github.com/laruss/pydantic-mongo), and a base controller.
The project also utilizes a `.env` file for database configuration and includes a `main.py` file as the entry point.

### Version: 1.1.1

## Features

- Flask server for creating RESTful API endpoints
- pydantic-mongo ODM for defining MongoDB models
- BaseController for inheriting controller functionality
- Configuration via .env file
- Local development with the option to connect to a remote MongoDB database

## Installation

1. Clone this repository:
    
```bash
    git clone https://github.com/laruss/database-controller-main.git
```
   
2. Navigate to the project directory:
        
```bash
       cd database-controller-main
```

3. Install the dependencies:
    
```bash
    pip install -r requirements.txt
```
   
4. Copy the `.env.sample` file to `.env` and update the values:
    
```bash
DB="sample"
DB_HOST="sample"
DB_PORT=27017
DB_ALIAS="default"
FLASK_APP_HOST=localhost
FLASK_APP_PORT=5002
FLASK_APP_NAME="sample"
DEBUG=1
```

5. Clone the frontend controller repository to the `frontend-controller` directory:
    
```bash
    git clone https://github.com/laruss/database-controller-front.git frontend-controller
````

6. Follow the instructions in readme.md of the `frontend-controller` directory.

7. Run the project:
    
```bash
    python main.py
```
   
8. Access the RESTful API endpoints via the browser, Postman, or other tools.

9. You are all set! Now you can start building your own project.
