"""base test file."""
import unittest

from bucketlist import create_app, db
from bucketlist.models import User, Bucketlist, Item


class BaseTestCase(unittest.TestCase):
    """Base configuration file for tests."""

    def setUp(self):
        """Set up the test database and test user."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(username="lynn",
                    email="lynn@gmail.com",
                    password="password")
        bucketlist = Bucketlist(bucketlist_title="Visit Paris", creator_id=1)
        item = Item(item_name="The Eiffel Tower",
                    description="Wrought iron lattice tower in France",
                    bucketlist_id=1)

        db.session.add(user)
        db.session.add(bucketlist)
        db.session.add(item)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        # db.session.commit()

        # set header
        self.auth_header = {'Authorization': user.encode_auth_token(user.id)}
        self.token = user.encode_auth_token(user.id)

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.run()
