from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from postApp.models import Post
from commentApp.models import Comment
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterViewTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.register_url = reverse('register')  # Update this if your path name is different

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)

    def test_get_all_users_authenticated(self):
        response = self.client.get(self.register_url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self):
        url = f"{self.register_url}{self.user.id}/"
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user(self):
        url = f"{self.register_url}{self.user.id}/"
        data = {"username": "updateduser"}
        response = self.client.put(url, data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_delete_user(self):
        url = f"{self.register_url}{self.user.id}/"
        response = self.client.delete(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

# API Tesing for PostView
class PostViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        self.post = Post.objects.create(
            title="Test Post",
            body="Test body content",
            author=self.user
        )

        self.list_url = reverse('posts-list')
        self.detail_url = reverse('posts-detail', args=[self.post.id])

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)

    def test_create_post(self):
        data = {
            "title": "New Post",
            "body": "Content here",
            "author": self.user.id
        }
        response = self.client.post(self.list_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        data = {
            "title": "Updated Title",
            "body": self.post.body,
            "author": self.user.id
        }
        response = self.client.put(self.detail_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_post(self):
        response = self.client.delete(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


# APITesing for CommentView

class CommentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        self.post = Post.objects.create(title="Sample Post", body="Post content", author=self.user)
        self.comment = Comment.objects.create(text="First comment", post=self.post, author=self.user)

        self.list_url = reverse('comments-list')
        self.detail_url = reverse('comments-detail', args=[self.comment.id])

    def test_list_comments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_retrieve_comment(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.comment.text)

    def test_create_comment(self):
        data = {
            "text": "New comment",
            "post": self.post.id,
            "author": self.user.id
        }
        response = self.client.post(self.list_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        data = {
            "text": "Updated comment",
            "post": self.post.id,
            "author": self.user.id
        }
        response = self.client.put(self.detail_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, "Updated comment")

    def test_delete_comment(self):
        response = self.client.delete(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())




