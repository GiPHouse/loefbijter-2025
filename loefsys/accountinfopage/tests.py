"""Module defining the tests for accountinfopage."""

from datetime import date

from django.test import Client, TestCase
from django.urls import reverse
from django_dynamic_fixture import G

from loefsys.groups.models import LoefbijterGroup
from loefsys.users.models import MemberDetails, Membership, User


class EditAccountInformationTestCase(TestCase):
    """Tests for account information modification for users."""

    def setUp(self):
        """Set up users and constants."""
        self.client = Client()
        self.user = G(
            User,
            email="user@user.nl",
            password="secret1",
            phone_number="+31612345678",
            nickname="A",
        )
        self.member = G(
            MemberDetails, user=self.user, birthday=date(2004, 1, 1), show_birthday=True
        )
        self.membership = G(Membership, member=self.member, start=date(2024, 1, 1))
        self.edit_url = reverse("accountinfoedit")

    def test_valid_form_submitted(self):
        """Test that when a valid form is submitted.

        The data should be changed.
        """
        form_data = {
            "phone_number": "+31612345000",
            "nickname": self.user.nickname,
            "display_name_preference": self.user.display_name_preference,
            "birthday": date(2003, 1, 1),
            "gender": self.member.gender,
            "show_birthday": self.member.show_birthday,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("accountinfoedit"), data=form_data)
        self.assertEqual(response.status_code, 302)  # expect redirect to account page
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="+31612345000")
        self.assertContains(response=response, text="2003-01-01")

    def test_invalid_form_submitted(self):
        """Test that when an invalid form is submitted.

        The data should not be changed (user form is incorrect, member form is okay).
        """
        form_data = {
            "phone_number": "+316123450001",
            "nickname": self.user.nickname,
            "display_name_preference": self.user.display_name_preference,
            "birthday": date(2003, 1, 1),
            "gender": self.member.gender,
            "show_birthday": self.member.show_birthday,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("accountinfoedit"), data=form_data)
        self.assertEqual(response.status_code, 200)  # expect to load same page again
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response=response, text="+316123450001")
        self.assertContains(response=response, text="+31612345678")
        self.assertNotContains(response=response, text="2003-01-01")
        self.assertContains(response=response, text="2004-01-01")

    def test_invalid_form_submitted_2(self):
        """Test that when an invalid form is submitted.

        The data should not be changed (user form is okay, member form is incorrect).
        """
        form_data = {
            "phone_number": "+31612345000",
            "nickname": self.user.nickname,
            "display_name_preference": self.user.display_name_preference,
            "birthday": date(2003, 1, 1),
            "show_birthday": self.member.show_birthday,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("accountinfoedit"), data=form_data)
        self.assertEqual(response.status_code, 200)  # expect to load same page again
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response=response, text="+31612345000")
        self.assertContains(response=response, text="+31612345678")
        self.assertNotContains(response=response, text="2003-01-01")
        self.assertContains(response=response, text="2004-01-01")


class UserTestCase(TestCase):
    """Tests for the account information display for users."""

    def setUp(self):
        """Set up user without groups and user with groups."""
        self.client = Client()
        self.user1 = G(
            User, email="user@user.nl", password="secret1", phone_number="0612345678"
        )

        self.group1 = G(
            LoefbijterGroup,
            name="Title",
            description="Description",
            date_foundation=date(2021, 1, 1),
            display_members=False,
        )
        self.group2 = G(
            LoefbijterGroup,
            name="Board",
            description="58e",
            date_foundation=date(2021, 1, 1),
            display_members=False,
        )
        self.user2 = G(
            User,
            email="user2@user2.nl",
            password="secret2",
            phone_number="0612345678",
            groups=[self.group1, self.group2],
        )

    def not_logged_in(self):
        """Test that not logged in users are redirected to the signup page."""
        response = self.client.get("/account/")
        self.assertRedirects(
            response=response, expected_url="/signup/", status_code=301
        )

    def test_user_without_groups(self):
        """Test that all user information is displayed, apart from groups when there are none."""  # noqa: E501
        self.client.force_login(user=self.user1)
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="user@user.nl")
        self.assertContains(response=response, text="0612345678")
        self.assertNotContains(response=response, text="Member")
        self.assertNotContains(response=response, text="My groups")

    def test_user_with_groups(self):
        """Test that groups are displayed when user has groups."""
        self.client.force_login(user=self.user2)
        response = self.client.get("/account/")
        self.assertContains(response=response, text="My groups")
        self.assertContains(response=response, text="Title")
        self.assertContains(response=response, text="Description")
        self.assertContains(response=response, text="Board")
        self.assertContains(response=response, text="58e")


class MemberTestCase(TestCase):
    """Tests for the account information display for members."""

    def setUp(self):
        """Set up member."""
        self.user = G(
            User, email="member@member.nl", password="secret", phone_number="0687654321"
        )
        self.member = G(
            MemberDetails, user=self.user, birthday=date(2004, 1, 1), show_birthday=True
        )

    def test_member(self):
        """Test that all member information is displayed."""
        G(Membership, member=self.member, start=date(2024, 1, 1))

        self.client.force_login(user=self.user)
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="member@member.nl")
        self.assertContains(response=response, text="0687654321")
        self.assertContains(response=response, text="Member")
        self.assertContains(response=response, text="2004-01-01")
        self.assertContains(response=response, text="2024-01-01")

    def test_member_without_membership(self):
        """Test that an exception is raised when a member has no membership."""
        self.client.force_login(user=self.user)
        with self.assertRaises(
            expected_exception=Exception, msg="Member has no membership"
        ):
            self.client.get("/account/")

    def test_member_with_multiple_memberships(self):
        """Test that the latest membership information gets displayed when there are multiple memberships."""  # noqa: E501
        G(Membership, member=self.member, start=date(2022, 1, 1))
        G(Membership, member=self.member, start=date(2023, 1, 1))

        self.client.force_login(user=self.user)
        response = self.client.get("/account/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response=response, text="2022-01-01")
        self.assertContains(response=response, text="2023-01-01")
