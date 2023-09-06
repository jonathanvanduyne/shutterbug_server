from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from shutterbugapi.models import ShutterbugUser

class ShutterbugUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.shutterbug_user = ShutterbugUser.objects.create(user=self.user, bio="Test bio", profile_image_url="test.jpg")

    def test_list_shutterbug_users(self):
        response = self.client.get('/shutterbug-users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_shutterbug_user(self):
        response = self.client.get(f'/shutterbug-users/{self.shutterbug_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_shutterbug_user(self):
        response = self.client.get('/shutterbug-users/999/')  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_shutterbug_user(self):
        new_bio = "Updated bio"
        new_profile_image_url = "updated.jpg"
        data = {
            "bio": new_bio,
            "profile_image_url": new_profile_image_url
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/shutterbug-users/{self.shutterbug_user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_shutterbug_user = ShutterbugUser.objects.get(id=self.shutterbug_user.id)
        self.assertEqual(updated_shutterbug_user.bio, new_bio)
        self.assertEqual(updated_shutterbug_user.profile_image_url, new_profile_image_url)

    def test_update_nonexistent_shutterbug_user(self):
        data = {
            "bio": "Updated bio",
            "profile_image_url": "updated.jpg"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/shutterbug-users/999/', data)  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
