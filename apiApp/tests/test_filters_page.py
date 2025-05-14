from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from postApp.models import Post  # adjust path based on your app
from commentApp.models import Comment
from django.urls import reverse


class PostViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create 15 posts
        for i in range(15):
            Post.objects.create(
                author=self.user,
                title=f"Test Post {i}",
                content=f"Test content {i}"
            )

    def test_pagination_default(self):
        url = reverse('post-list')  # Use the correct name from your router
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Default page size

    def test_pagination_second_page(self):
        url = reverse('post-list')
        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Remaining posts

    def test_filter_by_author(self):
        url = reverse('post-list')
        response = self.client.get(url, {'author': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

    def test_search_title(self):
        url = reverse('post-list')
        response = self.client.get(url, {'search': 'Post 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should match "Test Post 1" and possibly "Test Post 10-19"
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_ordering(self):
        url = reverse('post-list')
        response = self.client.get(url, {'ordering': '-id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_post_id = response.data['results'][0]['id']
        self.assertEqual(first_post_id, Post.objects.last().id)
