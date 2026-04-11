from django.test import TestCase

from .models import User


class AccountAccessTests(TestCase):
    def test_signup_creates_account_and_redirects_to_catalogue(self):
        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "newcollector",
                "email": "newcollector@example.com",
                "password1": "ShelfMagicPass123",
                "password2": "ShelfMagicPass123",
            },
        )

        self.assertRedirects(response, "/catalogue/")
        self.assertTrue(User.objects.filter(username="newcollector").exists())

    def test_account_page_redirects_anonymous_users_to_login(self):
        response = self.client.get("/accounts/me/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_login_redirects_to_catalogue_by_default(self):
        user = User.objects.create_user(username="collector", password="ShelfMagicPass123")

        response = self.client.post(
            "/accounts/login/",
            {
                "username": user.username,
                "password": "ShelfMagicPass123",
            },
        )

        self.assertRedirects(response, "/catalogue/")
