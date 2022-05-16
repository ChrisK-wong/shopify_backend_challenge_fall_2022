# Shopify Backend Developer Intern Challenge

## Inventory Tracking API

A REST API that allows the creation of inventory items that can be assigned to shipments. This API is built with Python, Flask, and SQLAlchemy using an SQLite database. Attached to this app is a frontend built with Flask templates that can be used to make all supported API calls. 

## Getting Started

Requires Python 3.6

- Clone respository
  ```
  $ git clone https://github.com/ChrisK-wong/shopify_backend_challenge_fall_2022.git
  ```
- Create virtual environment
    ```
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```
- Install dependencies
  ```
  $ pip install -r requirements.txt
  ```
- Create database

  ```
  $ python3 -c 'import api; create_database()'
  ```
- Run the app
  ```
  $ python3 run.py
  ```
  To run without the frontend, remoe these lines from run.py
  ```
  from frontend.web import web
  app.register_blueprint(web)
  ```

## Using the API
The API requres JSON to be sent for `POST` and `PUT` requests. This is done by setting ```"Content-Type: application/json"``` in the header of the request with the JSON data.
