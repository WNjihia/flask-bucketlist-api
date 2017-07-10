"""test_bucketlistitems.py."""
import json
from tests.test_setup import BaseTestCase


class ItemsTestCase(BaseTestCase):
    """This class contains tests for items."""

    def test_create_new_item(self):
        """Test for successful creation of an item."""
        payload = {'name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/1/items/",
                                    data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Item The Louvre has been added",
                         res_message['message'])

    def test_create_Item_with_invalid_name_format(self):
        """Test for creation of an item with an invalid name format."""
        payload = {'name': '[]**%',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/1/items/",
                                    data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid name format", res_message['message'])

    def test_create_item_that_exists(self):
        """Test for creation of an item that already exists."""
        payload = {'name': 'The Eiffel Tower',
                   'description': 'Wrought iron lattice tower in France'}
        response = self.client.post("/api/v1/bucketlists/1/items/",
                                    data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Item already exists!", res_message['message'])

    def test_create_item_with_non_existent_bucketlist(self):
        """Test creation of an item with non existent bucketlist."""
        payload = {'name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        response = self.client.post("/api/v1/bucketlists/15/items/",
                                    data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist not found!", res_message['message'])

    def test_get_all_bucketlistitems(self):
        """Test retrieval of items successfully."""
        response = self.client.get("/api/v1/bucketlists/1/items/",
                                   headers=self.set_header())
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertIn("The Eiffel Tower", res_message[0]['name'])

    def test_get_items_with_invalid_bucketList_id(self):
        """Test retrieval of items with invalid bucketlist ID."""
        response = self.client.get("/api/v1/bucketlists/15/items/",
                                   headers=self.set_header())
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist not found!", res_message['message'])

    def test_get_items_by_id(self):
        """Test retrieval of an item by ID."""
        response = self.client.get("/api/v1/bucketlists/1/items/1/",
                                   headers=self.set_header())
        self.assertEqual(response.status_code, 200)

    def test_update_item_by_id(self):
        """Test updating an item by ID."""
        payload = {'name': 'Just a tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/1/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Just a tower", res_message['message']['name'])

    def test_update_items_with_invalid_bucketList_id(self):
        """Test updating an item with invalid Bucketlist ID."""
        payload = {'name': 'The Eiffel Tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/15/items/1/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist not found!", res_message['message'])

    def test_update_item_that_does_not_exist(self):
        """Test updating an item that does not exist."""
        payload = {'name': 'The Eiffel Tower',
                   'description': 'Tallest building in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/15/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Item not found!", res_message['message'])

    def test_update_item_with_the_same_data(self):
        """Test updating an item with the same data."""
        payload = {'name': 'The Eiffel Tower',
                   'description': 'Wrought iron lattice tower in France'}
        response = self.client.put("/api/v1/bucketlists/1/items/1/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 409)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("No updates detected",
                         res_message['message'])

    def test_delete_item_successfully(self):
        """Test deleting an item by ID."""
        payload = {'name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        self.client.post("/api/v1/bucketlists/1/items/",
                         data=json.dumps(payload),
                         headers=self.set_header(),
                         content_type="application/json")
        response = self.client.delete("/api/v1/bucketlists/1/items/2/",
                                      headers=self.set_header())
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Item succesfully deleted", res_message['message'])

    def test_delete_item_that_does_not_exist(self):
        """Test deleting an item that does not exist."""
        response = self.client.delete("/api/v1/bucketlists/1/items/15/",
                                      headers=self.set_header(),)
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Item not found!", res_message['message'])

    def test_delete_items_with_invalid_bucketList_id(self):
        """Test deleting an item with an invalid bucketlist ID."""
        response = self.client.delete("/api/v1/bucketlists/5/items/1/",
                                      headers=self.set_header(),)
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist not found!", res_message['message'])

    def test_change_item_status(self):
        """Test change of item status"""
        payload = {'name': 'The Louvre',
                   'description': 'Largest museum in Paris'}
        self.client.post("/api/v1/bucketlists/1/items/",
                         data=json.dumps(payload),
                         headers=self.set_header(),
                         content_type="application/json")
        response = self.client.get("/api/v1/bucketlists/1/items/2/",
                                   data=json.dumps(payload),
                                   headers=self.set_header())
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual(res_message['status'], 'Not done')

        payload = {'is_completed': 'True'}
        response = self.client.put("/api/v1/bucketlists/1/items/2/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual(res_message['message']['completion_status'], 'Done')
