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
  $ python3 -c 'import api; api.create_database()'
  ```
- Run the app
  ```
  $ python3 run.py
  ```
  To run without the frontend, remove these lines from run.py
  ```
  from frontend import create_webapp
  create_webapp(app)
  ```

## Using the API
The API receives and returns JSON data. JSON data is required for `POST` and `PUT` requests. This is done by setting ```"Content-Type: application/json"``` in the header of the request with the JSON data in the body of the request.


### Inventory Items
The `/api/items` route is used to make CRUD requests for items. Items are stored in a table with columns: `id`, `name`, and `quantity`.
|Endpoint|HTTP VERB|Result|Sample Request Body|Sample Response|
|--------|---------|------|-------------------|---------------|
| /api/items | GET | Returns all inventory items in the database | | <pre lang="json">[&#13;  {&#13;    "id": 1,&#13;    "name": "Pen",&#13;    "quantity": 40&#13;  },&#13;  {&#13;    "id": 2,&#13;    "name": "Notebook",&#13;    "quantity": 15&#13;  }&#13;]</prev>
| /api/items | POST | Adds a new inventory item into database | <pre lang="json">{&#13;  "name": "Pen",&#13;  "quantity": 40&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/items/:id | GET | Returns data of an inventory item | | <pre lang="json">{&#13;  "id": 1,&#13;  "name": "Pen",&#13;  "quantity": 40&#13;}</pre> |
| /api/items/:id/update | PUT | Updates an inventory item's data | <pre lang="json">{&#13;  "name": "Pencil",&#13;  "quantity": 20&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/items/:id | DELETE | Deletes an inventory item from database | | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |

### Shipments
The `/api/shipments` route is used to make CRUD requests for shipments. Shipments are stored in a table with columns: `id`, `description` and `address`.
Items from inventory can also be stored into shipments and this information is stored in a many-to-many association table with the columns `id`, `ship_id`, `item_id`, and `quantity`.
|Endpoint|HTTP VERB|Result|Sample Request Body|Sample Response|
|--------|---------|------|-------------------|---------------|
| /api/shipments | GET | Returns all shipments in the database | | <pre lang="json">[&#13;  {&#13;    "address": "123 Class Ave...USA",&#13;    "description": "School Supplies",&#13;    "id": 1,&#13;    "items": [&#13;      {&#13;        "item_id": 2,&#13;        "name": "Notebook",&#13;        "quantity": 10&#13;      },&#13;      {&#13;        "item_id": 4,&#13;        "name": "100 x Paper",&#13;        "quantity": 30&#13;      }&#13;    ]&#13;  },&#13;  {&#13;    "address": "321 Joe Street...USA",&#13;    "description": "Trader Joes",&#13;    "id": 2,&#13;    "items": [&#13;      {&#13;        "item_id": 3,&#13;        "name": "Apple",&#13;        "quantity": 12&#13;      }&#13;    ]&#13;  }&#13;]</prev> |
| /api/shipments | POST | Adds a new shipment into database | <pre lang="json">{&#13;  "description": "School Supplies",&#13;  "address": "123 Class Ave...USA"&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/shipments/:id | GET | Returns data of a shipment | | <pre lang="json">{&#13;  "description": "Trader Joes",&#13;  "address": "321 Joe Street...USA",&#13;  "id": 2,&#13;  "items": [&#13;    {&#13;      "item_id": 3,&#13;      "name": "Apple",&#13;      "quantity": 12&#13;    }&#13;  ]&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}
| /api/shipments/:id/update | PUT | Updates a shipment's data | <pre lang="json">{&#13;  "description": "School Stuff",&#13;  "address": "124 Class Ave...USA"&#13;} | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/shipments/:id/delete | DELETE | Deletes a shipment from database | | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/shipments/:id/add | POST | Adds an item to shipment | <pre lang="json">{&#13;  "item_id": 1,&#13;  "quantity": 30&#13;}</pre> | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |
| /api/shipments/:id/:item_id/remove | DELETE | Removes an item from shipment | | <pre lang="json">{&#13;  "success": "true"&#13;}</pre> |

