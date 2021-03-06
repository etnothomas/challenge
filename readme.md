# Run the Project
In the /challenge/src/app folder run the app.py file. This will start a flask application, with a sqlite3 backend.

Packages used (also in the requirements file):
- sqlalchemy
- numpy
- flask


# Usage of the API
## Create  a New Global Capacity
http://localhost:5050/archlet/v1/postglobalcapacity

Creates a new global capacity model. The user has to set the content type to 'application/json' in the header. It takes a body like this:

```json
{
    "supplier": "clariant",
    "capacity": 100
}
```
## Create a New Regional Capacity
http://localhost:5050/archlet/v1/postregionalcapacity

Create a new regional capacity model. The user has to set the content type to 'application/json' in the header. It takes a body like this:

```json
{
    "supplier": "Clariant",
    "country_supplier": "Argentina",
    "region": "South America",
    "country_destination": "Mexico",
    "type": "Standard",
    "capacity": 100
}
```

## Create/Update an Offer
http://localhost:5050/archlet/v1/postitemcapacity

Create or update an offer. If an object already exists with the same item, supplier and project id, it will get updated, otherwise a new object will be created. The user has to set the content type to 'application/json' in the header. It takes a body like this:

```json
{
    "supplier": "Clariant",
    "item": "Item_0001",
    "project_id": "33aad28d-59f5-4b9f-bee8-ebe1a2389570",
    "unit_price": 200.0,
    "capacity": 100
}
```

## Get Regional and Global Capacities for Project

http://localhost:5050/archlet/v1/getregionalandglobalcapacitieswithoffers?project_id=<some-id>

This takes a project id as a query parameter, and return a list of jsons with the same project id, like below, indexed by supplier and region

```json
{
  "33aad28d-59f5-4b9f-bee8-ebe1a2389570": {
    "clariant": {
      "europe": [
        {"supplier": "clariant", 
          "region": "europe", 
          "country_supplier": "india",
          "country_destination": "great", 
          "global_cap": "3500000", 
          "regional_cap": "16388"}
      ]
    }
  }
}
```

## Get Regional and Global Capacities and Their Offers

http://localhost:5050/archlet/v1/getprojectregionalandglobalcaps

This does not take any query parameter. Returns a list of jsons like below, indexed by item, supplier and region:

```json
{
  "clariant": {
    "europe": {
      "Item_0001": [
        {"supplier": "clariant", 
          "region": "europe", 
          "country_supplier": "india", 
          "country_destination": "great", 
          "global_cap": "3500000", 
          "regional_cap": "16388", 
          "item": "Item_0001"}
      ]
    }
  }
}
```

## Get Offer Capacities

http://localhost:5050/archlet/v1/archlet/v1/getoffercapacities?item_id=<some-id>

This takes an item id as a query parameter. Returns a list of jsons with the same item id, like below, indexed by item,supplier, region

```json
{
  "Item_0001": {
    "clariant": {
      "europe": [
        {"item": "Item_0001", 
          "supplier": "clariant", 
          "item_cap": null, 
          "region": "europe", 
          "country_supplier": "india", 
          "country_destination": "great", 
          "global_cap": "3500000", 
          "regional_cap": "16388", 
          "unit_price": "187.2700000000"}
      ]
    }
  }
}
```

## Issues
1. global capacity is reported on every item at the lowest granularity, could be a separate key
2.  some verbose code when getting data from the database, that repeats, could be refactored
3.  instead of relying on the itertools library to group items, this could be pushed to the database with some better modelling
4.  api names... pretty verbose...
5.  money modelling should be Decimal, but sqlite does not support that apparently...
6.  tail recursion
7.  should add type hints
8.  swagger would be nice
9.  better relationship between tables, to remove boileplate code in the database retrieval (see 2)