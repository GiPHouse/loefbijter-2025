"""Module defining the tests for profile."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

settings.LANGUAGE_CODE = "en"

User = get_user_model()


class LoginTestCase(TestCase):
    """Tests for signing up and logging in."""

    def setUp(self):
        """Set up the needed variables for the tests."""
        self.client = Client()
        self.email = "user@user.nl"
        self.new_email = "new.user@email.com"
        self.password = "password"
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            phone_number="+31612345678",
            nickname="Naam",
            picture=None,
        )

    def test_login_page(self):
        """Tests if the login page is rightfully loaded."""
        response = self.client.get(reverse("login"))
        self.assertContains(response, "Login")

    def test_invalid_credentials_login(self):
        """Tests if invalid credentails are rightfully handled."""
        form_data_wrong_email = {
            "username": "notuser@user.nl",
            "password": self.password,
        }
        form_data_wrong_password = {
            "username": self.email,
            "password": "notthepassword",
        }
        response = self.client.post(
            reverse("login"), data=form_data_wrong_email, follow=True
        )
        self.assertContains(response, "Please enter a correct email and password.")

        response = self.client.post(
            reverse("login"), data=form_data_wrong_password, follow=True
        )
        self.assertContains(response, "Please enter a correct email and password.")

    def test_login(self):
        """Tests if a user can login."""
        form_data = {"username": self.email, "password": self.password}
        response = self.client.post(reverse("login"), data=form_data, follow=True)
        self.assertContains(response, "Personal details")
        user = response.context["user"]
        self.assertTrue(user.is_authenticated)

    def test_signup_existing_acc(self):
        """Tests that you can not sign up with an existing email."""
        form_data = {
            "email": self.email,
            "password1": "DiffPass!",
            "password2": "DiffPass!",
        }
        response = self.client.post(reverse("signup"), data=form_data, follow=True)
        self.assertContains(response, "User with this Email already exists.")
        self.assertTrue(self.user)

    def test_signup_invalid_password(self):
        """Tests that you can not sign up with an inval password."""
        form_data_personal_info = {
            "email": self.new_email,
            "password1": self.new_email,
            "password2": self.new_email,
        }

        form_data_short = {
            "email": self.new_email,
            "password1": "short",
            "password2": "short",
        }
        form_data_common = {
            "email": self.new_email,
            "password1": "password123",
            "password2": "password123",
        }
        form_data_num = {
            "email": self.new_email,
            "password1": "759268743605729084",
            "password2": "759268743605729084",
        }

        response = self.client.post(
            reverse("signup"), data=form_data_personal_info, follow=True
        )
        self.assertContains(response, "The password is too similar to the email.")

        response = self.client.post(
            reverse("signup"), data=form_data_short, follow=True
        )
        self.assertContains(
            response,
            "This password is too short. It must contain at least 8 characters.",
        )

        response = self.client.post(
            reverse("signup"), data=form_data_common, follow=True
        )
        self.assertContains(response, "This password is too common.")

        response = self.client.post(reverse("signup"), data=form_data_num, follow=True)
        self.assertContains(response, "This password is entirely numeric.")

    def test_signup_diff_password(self):
        """Tests that if you enter 2 different passwords it denies the request."""
        form_data = {
            "email": self.new_email,
            "password1": self.password,
            "password2": "Diffpass!",
        }
        response = self.client.post(reverse("signup"), data=form_data, follow=True)
        self.assertContains(response, "The two password fields didn’t match.")  # noqa: RUF001

    def test_signup(self):
        """Test for when a valid signup is performed, a user is created."""
        user = get_user_model()

        # check that user does not exist at first
        self.assertFalse(user.objects.filter(email="user2@user.com").exists())

        form_data = {
            "email": "user2@user.com",
            "password1": "Hardpassword#2",
            "password2": "Hardpassword#2",
        }

        self.client.post(reverse("signup"), data=form_data, follow=True)

        self.assertTrue(user.objects.filter(email="user2@user.com").exists())
