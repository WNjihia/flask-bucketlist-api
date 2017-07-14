"""test_user_auth.py."""
import json
from tests.test_setup import BaseTestCase


class UserAuthTestCase(BaseTestCase):
    """This class contains tests for user registration and log in."""

    LOGIN_URL = "/api/v1/auth/login"
    REGISTER_URL = "/api/v1/auth/register"

    def test_successful_user_registration(self):
        """Test for successful user registration."""
        self.payload = dict(username='test_username',
                            email='user@test.com',
                            password='123456789'
                            )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("You have been successfully registered.",
                      str(response.data))

    def test_user_registration_with_short_password(self):
        """Test for successful user registration."""
        self.payload = dict(username='test_username',
                            email='user@test.com',
                            password='1234'
                            )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password too short!",
                      str(response.data))

    def test_user_registration_when_user_already_exists(self):
        """Test registration of an already existing user."""
        self.payload = dict(username='test_username',
                            email='user@test.com',
                            password='123456789'
                            )
        self.client.post(self.REGISTER_URL, data=json.dumps(self.payload),
                         content_type="application/json")
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists!", str(response.data))

    def test_user_registration_with_no_email(self):
        """Test for user registration with no email."""
        self.payload = dict(username='test_username',
                            password='123456789',
                            email=''
                            )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Please provide an email!", res_message['message'])

    def test_user_registration_with_invalid_email_format(self):
        """Test for user registration with invalid email format."""
        self.payload = dict(username='test_username',
                            email='memi.gmail',
                            password='123456789'
                            )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid email!", res_message['message'])

    def test_user_registration_with_empty_username(self):
        """Test for user registration with empty username."""
        self.payload = dict(username='',
                            email='user@test.com',
                            password='123456789'
                            )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Please provide a username!", res_message['message'])

    def test_user_registration_username_already_exists(self):
        """Test for registration with an already existing username."""
        self.payload = dict(username='test_username',
                            email='user@test.com',
                            password='123456789'
                            )
        self.client.post(self.REGISTER_URL, data=json.dumps(self.payload),
                         content_type="application/json")
        self.data = dict(username='test_username',
                         email='me@user.com',
                         password='453256789'
                         )
        response = self.client.post(self.REGISTER_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("User already exists!",
                         res_message['message'])

    def test_user_login(self):
        """Test for successful user login."""
        self.payload = dict(email="lynn@gmail.com",
                            password="password"
                            )
        response = self.client.post(self.LOGIN_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("You have successfully logged in.",
                         res_message['message'])

    def test_user_login_with_invalid_credentials(self):
        """Test for user login with invalid user credentials."""
        self.payload = dict(email="johndoe@gmail.com",
                            password="johnny12"
                            )
        response = self.client.post(self.LOGIN_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid username/password!", res_message['message'])

        self.payload = dict(email="me@gmail.com",
                            password="ohndoe12"
                            )
        response = self.client.post(self.LOGIN_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid username/password!", res_message['message'])

    # repetitive test
    def test_user_login_with_unregistered_user(self):
        """Test for login with an unregistered user."""
        self.payload = dict(email="jane@gmail.com",
                            password="jane1234"
                            )
        response = self.client.post(self.LOGIN_URL,
                                    data=json.dumps(self.payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        res_message = json.loads(response.data.decode('utf8'))
        self.assertEqual("Invalid username/password!", res_message['message'])
