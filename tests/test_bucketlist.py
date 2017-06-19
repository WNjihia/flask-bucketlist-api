"""test_bucketlist.py."""
import json
from tests.test_setup import BaseTestCase


class BucketListTestCase(BaseTestCase):
    """This class contains tests for the bucketlist."""

    URL = "/api/v1/bucketlists/"

    def test_create_new_BucketList(self):
        """Test for successful creation of a bucketlist."""
        payload = {'bucketlist_title': 'Visit Kenya'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual("Bucketlist created successfully", str(response.data))

    def test_create_BucketList_that_exists(self):
        """Test for creation of a bucketlist that already exists."""
        payload = {'bucketlist_title': 'Visit Paris'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("This bucketlist already exists", str(response.data))

    def test_get_all_BucketLists(self):
        """Test for retrieval of all bucketlists."""
        response = self.client.get(self.URL, headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Visit Paris", str(response.data))

    def test_get_BucketList_by_id(self):
        """Test for retrieval of a bucketlists by id."""
        # Get bucketlist with ID 1
        response = self.client.get("/api/v1/bucketlists/1",
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200)

        # Get bucketlist with ID 2
        payload = {'bucketlist_title': 'Visit Rome'}
        response = self.client.post(self.URL, data=json.dumps(payload),
                                    headers=self.auth_header,
                                    content_type="application/json")
        response = self.client.get("/api/v1/bucketlists/2")
        self.assertEqual(response.status_code, 200)

    def test_get_BucketList_that_does_not_exist(self):
        """Test for retrieval of a bucketlists that does not exist."""
        response = self.client.get("/api/v1/bucketlists/15",
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_update_BucketList_by_id(self):
        """Test for updating a bucketlists by id."""
        payload = {'bucketlist_title': 'Visit Israel'}
        response = self.client.put("/api/v1/bucketlists/1",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Bucketlist succesfully updated", str(response.data))

    def test_update_BucketList_that_does_not_exist(self):
        """Test for updating a bucketlists that does not exist."""
        payload = {'bucketlist_title': 'Visit Israel'}
        response = self.client.put("/api/v1/bucketlists/15",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))

    def test_update_BucketList_with_the_same_data(self):
        # code 409
        """Test for updating a bucketlists with the same data."""
        payload = {'bucketlist_title': 'Visit Paris'}
        response = self.client.put("/api/v1/bucketlists/1",
                                   data=json.dumps(payload),
                                   headers=self.auth_header,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual("No updates detected",
                         str(response.data))

    def test_delete_BucketList_by_id(self):
        """Test for deleting a bucketlist succesfully."""
        response = self.client.delete("/api/v1/bucketlists/1",
                                      headers=self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Bucketlist succesfully deleted", str(response.data))

    def test_delete_BucketList_that_does_not_exist(self):
        """Test for deleting a bucketlist that does not exist."""
        response = self.client.delete("/api/v1/bucketlists/15",
                                      headers=self.auth_header)
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Bucketlist cannot be found", str(response.data))
