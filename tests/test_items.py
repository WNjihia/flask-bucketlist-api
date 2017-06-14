"""test_bucketlistitems.py."""
import json
from tests.test import BaseTestCase


class ItemsTestCase(BaseTestCase):
    """This class contains tests for items."""

    def test_createItem(self):
        """Test for successful creation of an item."""
        data = {'item_name': 'The Louvre',
                'description': 'Largest museum in Paris'}
        response = self.client().post("/api/v1/bucketlists/1/items",
                                      json.dumps(data),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual("Item created successfully", str(response.data))

    def test_createItem_with_invalid_name_format(self):
        """Test for creation of an item with an invalid name format."""
        data = {'item_name': '1234%$#@!^&',
                'description': 'Largest museum in Paris'}
        response = self.client().post("/api/v1/bucketlists/1/items",
                                      json.dumps(data),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Invalid format", str(response.data))

    def test_createItem_that_exists(self):
        """Test for creation of an item that already exists."""
        data = {'item_name': 'The Eiffel Tower',
                'description': 'Wrought iron lattice tower in France'}
        response = self.client().post("/api/v1/bucketlists/1/items",
                                      json.dumps(data),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("This item already exists", str(response.data))

    def test_createItem_with_non_existent_bucketlist(self):
        """Test creation of an item with non existent bucketlist."""
        data = {'item_name': 'The Louvre',
                'description': 'Largest museum in Paris'}
        response = self.client().post("/api/v1/bucketlists/15/items",
                                      json.dumps(data),
                                      content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_getBucketListItems(self):
        """Test retrieval of items successfully."""
        data = {'item_name': 'The Louvre',
                'description': 'Largest museum in Paris'}
        self.client().post("/api/v1/bucketlists/1/items", json.dumps(data),
                           content_type="application/json")
        response = self.client().get("/api/v1/bucketlists/1/items")
        self.assertEqual(response.status_code, 200)

    def test_getItems_with_invalid_BucketList_Id(self):
        """Test retrieval of items with invalid bucketlist ID."""
        response = self.client().get("/api/v1/bucketlists/15/items")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_getItems_by_id(self):
        """Test retrieval of an item by ID."""
        response = self.client().get("/api/v1/bucketlists/1/items/1")
        self.assertEqual(response.status_code, 200)

    def test_updateItem_by_id(self):
        """Test updating an item by ID."""
        data = {'item_name': 'The Eiffel Tower',
                'description': 'Tallest building in France'}
        response = self.client().put("/api/v1/bucketlists/1/items/1",
                                     json.dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual("Item succesfully updated", str(response.data))

    def test_updateItems_with_invalid_BucketList_Id(self):
        """Test updating an item with invalid Bucketlist ID."""
        data = {'item_name': 'The Eiffel Tower',
                'description': 'Tallest building in France'}
        response = self.client().put("/api/v1/bucketlists/15/items/1",
                                     json.dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_updateItem_that_does_not_exists(self):
        """Test updating an item that does not exist."""
        data = {'item_name': 'The Eiffel Tower',
                'description': 'Tallest building in France'}
        response = self.client().put("/api/v1/bucketlists/1/items/15",
                                     json.dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Item cannot be found", str(response.data))

    def test_updateItem_with_same_data(self):
        """Test updating an item with the same data."""
        data = {'item_name': 'The Eiffel Tower',
                'description': 'Wrought iron lattice tower in France'}
        response = self.client().put("/api/v1/bucketlists/1/items/1",
                                     json.dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual("There is a conflict in the update",
                         str(response.data))

    def test_deleteItem_by_id(self):
        """Test deleting an item by ID."""
        response = self.client().delete("/api/v1/bucketlists/1/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Item succesfully deleted", str(response.data))

    def test_deleteItem_that_does_not_exist(self):
        """Test deleting an item that does not exist."""
        response = self.client().delete("/api/v1/bucketlists/1/items/15")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Item cannot be found", str(response.data))

    def test_deleteItems_with_invalid_BucketList_Id(self):
        """Test deleting an item with an invalid bucketlist ID."""
        response = self.client().delete("/api/v1/bucketlists/5/items/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_changeItemstatus(self):
        pass
