from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from shutterbugapi.models import ShutterbugUser, Category

class CategoryViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.shutterbug_user = ShutterbugUser.objects.create(user=self.user)
        self.category = Category.objects.create(label="Test Category")

    def test_list_categories(self):
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        response = self.client.get(f'/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_category(self):
        response = self.client.get('/categories/999/')  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_category(self):
        data = {"label": "New Category"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_category = Category.objects.get(label="New Category")
        self.assertIsNotNone(new_category)

    def test_create_category_without_label(self):
        data = {}  # Missing 'label' field
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category(self):
        new_label = "Updated Category"
        data = {"label": new_label}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/categories/{self.category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.label, new_label)

    def test_update_category_without_label(self):
        data = {}  # Missing 'label' field
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f'/categories/{self.category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category.id)

    def test_destroy_nonexistent_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/categories/999/')  # Assuming 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
