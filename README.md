# E-Commerce Project

This is a simple e-commerce web application built with Flask and MySQL.

## Features

- User authentication
- Product listing
- Shopping cart
- Order management
- Admin panel

## Requirements

- Python 3.10
- Flask
- MySQL
- pytz
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/hoangluu18/e_commerce.git
   cd e_commerce
   ```

2. Create and activate a virtual environment:
   ```sh
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database.
   - Update the `.env` file with your database credentials.

5. Run the database migrations:
   ```sh
   flask db upgrade
   ```

## Running the Application

1. Set the `FLASK_APP` environment variable:
   ```sh
   export FLASK_APP=e_commerce/index.py  # On Windows use `set FLASK_APP=e_commerce/index.py`
   ```

2. Start the Flask application:
   ```sh
   flask run
   ```

## Deployment

Follow the steps to deploy the application on PythonAnywhere as described in the previous instructions.
