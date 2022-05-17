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
  To run without the frontend, remove these lines from run.py
  ```
  from frontend.web import web
  app.register_blueprint(web)
  ```

## Using the API
The API receives and returns JSON data. JSON data is required for `POST` and `PUT` requests. This is done by setting ```"Content-Type: application/json"``` in the header of the request with the JSON data in the body of the request.


### Inventory Items
|Endpoint|HTTP VERB|Result|Sample Request Body|Sample Response|
|--------|---------|------|-------------------|---------------|
| /api/items | GET | Returns all inventory items in the database | | <pre lang="json">[&#13;  {&#13;    "id": 1,&#13;    "name": "Pen",&#13;    "quantity": 40&#13;  },&#13;  {&#13;    "id": 2,&#13;    "name": "Notebook",&#13;    "quantity": 15&#13;  }&#13;]</prev>
| /api/items | POST | Adds a new inventory item into database | <pre lang="json">{&#13;  "name": "Pen",&#13;  "quantity": 40&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/items/:id | GET | Returns data of an inventory item | | <pre lang="json">{&#13;  "id": 1,&#13;  "name": "Pen",&#13;  "quantity": 40&#13;}</pre> |
| /api/items/:id/update | PUT | Updates an inventory item's data | <pre lang="json">{&#13;  "name": "Pencil",&#13;  "quantity": 20&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/items/:id | DELETE | Deletes an inventory item from the database | | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |

