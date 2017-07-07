"""test_bucketlist.py."""
import json
from tests.test_setup import BaseTestCase


class BucketListTestCase(BaseTestCase):
    """This class contains tests for the bucketlist."""

    URL = "/api/v1/bucketlists/"

    def test_create_new_bucketlist(self):
        """Test for successful creation of a bucketlist."""
        payload = {'title': 'Visit Kenya'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist Visit Kenya has been added",
                         res_message['message'])

    def test_create_new_bucketlist_with_invalid_name_format(self):
        """Test for creation of a bucketlist with invalid name format."""
        payload = {'title': ''}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid bucketlist title!", res_message['message'])

        payload = {'title': '@#$%^**^%$'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid bucketlist title!", res_message['message'])

    def test_create_bucketlist_that_exists(self):
        """Test for creation of a bucketlist that already exists."""
        payload = {'title': 'Visit Paris'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.set_header(),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertIn("Bucketlist already exists!", res_message['message'])

    def test_get_all_bucketlists(self):
        """Test for retrieval of all bucketlists."""
        response = self.client.get(self.URL, headers=self.set_header())
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertIn("Visit Paris", res_message[0]['title'])

    def test_get_bucketlist_by_id(self):
        """Test for retrieval of a bucketlists by id."""
        # Get bucketlist with ID 1
        response = self.client.get("/api/v1/bucketlists/1/",
                                   headers=self.set_header())
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual('Visit Paris', res_message['title'])

    def test_get_bucketlist_that_does_not_exist(self):
        """Test for retrieval of a bucketlists that does not exist."""
        response = self.client.get("/api/v1/bucketlists/15/",
                                   headers=self.set_header())
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist cannot be found", res_message['message'])

    def test_update_bucketlist_successfully(self):
        """Test for updating a bucketlists by id."""
        payload = {'title': 'Visit Israel'}
        response = self.client.put("/api/v1/bucketlists/1/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Visit Israel", res_message['message']['title'])

    def test_update_bucketlist_that_does_not_exist(self):
        """Test for updating a bucketlist that does not exist."""
        payload = {'title': 'Visit Israel'}
        response = self.client.put("/api/v1/bucketlists/15/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist does not exist!", res_message['message'])

    def test_update_bucketlist_with_the_same_data(self):
        """Test for updating a bucketlist with the same data."""
        payload = {'title': 'Visit Paris'}
        response = self.client.put("/api/v1/bucketlists/1/",
                                   data=json.dumps(payload),
                                   headers=self.set_header(),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 409)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("No updates detected",
                         res_message['message'])

    def test_delete_bucketlist_successfully(self):
        """Test for deleting a bucketlist succesfully."""
        response = self.client.delete("/api/v1/bucketlists/1/",
                                      headers=self.set_header())
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist successfully deleted!",
                         res_message['message'])

    def test_delete_bucketlist_that_does_not_exist(self):
        """Test for deleting a bucketlist that does not exist."""
        response = self.client.delete("/api/v1/bucketlists/15/",
                                      headers=self.set_header())
        self.assertEqual(response.status_code, 404)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Bucketlist cannot be found", res_message['message'])
