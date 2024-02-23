Overview
---------
This API has below user stories implemented from FastAPI:

* As a company, I want all my products in a database, so I can offer them via our new platform to customers
* As a client, I want to add a product to my shopping cart, so I can order it at a later stage
* As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need
* As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car
* As a client, I want to select a delivery date and time, so I will be there to receive the order
* As a client, I want to see an overview of all the products, so I can choose which product I want
* As a client, I want to view the details of a product, so I can see if the product satisfies my needs


Special Notes
--------------
## Assumptions and limitations

### Limitations
* Only basic validations are included and edge cases may fail.
* Atomic operation are not implemented for handling Stock on hand quantity when adding/deleting items to cart.
* Unit tests were not implemented due to the limited time.
* Pagination is not available for list endpoints. E.g list_products

### Assumptions
* There'll be a separate authentication service and user_service which allows to register users and do their authentication.

How To Run it
--------------
## Running with Docker

#### 1. Build the image

```shell
docker compose build
```

#### 2. Run the services

```shell
docker compose up
```
Swagger UI:  [http://localhost:8010/docs#/)

## Setting up App locally

#### 1. System Requirements

```shell
python 3.11
```

#### 2. Install Requirements

```shell
make setup
make install
```

#### 3. Set Environments variables

Environment variables needed to run the app
```shell
export DB_URL=<db-url>
```
E.g.
```
postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>
```
