from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from shutterbugapi.models import ShutterbugUser, Post, Category

class PostViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a test category
        self.category = Category.objects.create(label="Test Category")

        # Create a test post
        self.post = Post.objects.create(
            shutterbug_user=ShutterbugUser.objects.get(user=self.user),
            title="Test Post",
            image_url="https://example.com/test.jpg",
            content="Test content",
            published_on="2023-01-01T00:00:00Z",
            category=self.category,
            approved=True,
            flagged=False
        )

    def test_list_posts(self):
        url = '/posts/'
        client = APIClient()
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post(self):
        url = f'/posts/{self.post.id}/'
        client = APIClient()
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        url = '/posts/'
        data = {
            "title": "New Post",
            "image_url": "https://example.com/new.jpg",
            "content": "New content",
            "published_on": "2023-01-02T00:00:00Z",
            "category": self.category.id,
            "approved": True,
            "flagged": False
        }

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        url = f'/posts/{self.post.id}/'
        data = {
            "title": "Updated Post",
            "image_url": "https://example.com/updated.jpg",
            "content": "Updated content",
            "published_on": "2023-01-03T00:00:00Z",
            "category": self.category.id,
            "approved": False,
            "flagged": True
        }

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post(self):
        url = f'/posts/{self.post.id}/'

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
