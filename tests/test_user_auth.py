"""test_user_auth.py."""
import json
from tests.test_setup import BaseTestCase


class UserAuthTestCase(BaseTestCase):
    """This class contains tests for user registration and log in."""

    LOGIN_URL = "/api/v1/auth/login"
    REGISTER_URL = "/api/v1/auth/register"

    def test_user_registration(self):
        """Test for successful user registration."""
        self.data = {'username': 'test_username',
                     'email': 'user@test.com',
                     'password': '1234'
                     }
        response = self.client.post(self.REGISTER_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual("You have successfully registered.",
                         str(response.data))

    def test_user_registration_when_user_already_exists(self):
        """Test registration of an already existing user."""
        self.data = {'username': 'test_username',
                     'email': 'user@test.com',
                     'password': '1234'
                     }
        self.client.post(self.REGISTER_URL, json.dumps(self.data),
                         content_type="application/json")
        response = self.client.post(self.REGISTER_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("User already exists!", str(response.data))

    def test_user_registration_with_no_email(self):
        """Test for user registration with no email."""
        self.data = {'username': 'test_username',
                     'password': '1234'
                     }
        response = self.client.post(self.REGISTER_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("Please provide an email!", str(response.data))

    def test_user_registration_username_already_exists(self):
        """Test for registration with an already existing username."""
        self.data = {'username': 'test_username',
                     'email': 'user@test.com',
                     'password': '1234'
                     }
        self.data.post(self.REGISTER_URL, json.dumps(self.data),
                       content_type="application/json")
        self.data = {'username': 'test_username',
                     'email': 'me@user.com',
                     'password': '56789'
                     }
        response = self.client.post(self.REGISTER_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("Username already exists! Please provide another",
                         str(response.data))

    def test_user_login(self):
        """Test for successful user login."""
        self.data = {'username': "johndoe",
                     'email': "johndoe@gmail.com"
                     }
        response = self.data.post(self.LOGIN_URL, json.dumps(self.data),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("You have successfully logged in",
                         str(response.data))

    def test_user_login_with_invalid_credentials(self):
        """Test for user login with invalid user credentials."""
        self.data = {'username': "johnny",
                     'email': "johndoe@gmail.com"
                     }
        response = self.data.post(self.LOGIN_URL, json.dumps(self.data),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("Invalid username/password!", str(response.data))

        self.data = {'username': "johndoe",
                     'email': "me@gmail.com"
                     }
        response = self.client.post(self.LOGIN_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual("Invalid username/password!", str(response.data))

    def test_user_login_with_unregistered_user(self):
        """Test for login with an unregistered user."""
        self.data = {'username': "jane",
                     'email': "jane@gmail.com"
                     }
        response = self.client.post(self.LOGIN_URL, json.dumps(self.data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual("Invalid username/password!", str(response.data))
