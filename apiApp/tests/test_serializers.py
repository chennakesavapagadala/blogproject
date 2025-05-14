from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from apiApp.serializers import RegisterSerializer, CommentSerializer,PostSerializer  # adjust as needed

class RegisterSerializerTest(TestCase):
    def test_valid_data_creates_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.username, "testuser")

    def test_missing_password_raises_error(self):
        data = {
            "username": "nopassworduser",
            "email": "no@pass.com"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


from postApp.models import Post
from commentApp.models import Comment

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Post content')
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='Nice one!')

    def test_post_with_comments_serialized(self):
        serializer = PostSerializer(self.post)
        self.assertEqual(serializer.data['title'], 'Test Post')
        self.assertEqual(len(serializer.data['comments']), 1)
        self.assertEqual(serializer.data['comments'][0]['content'], 'Nice one!')

    def test_post_create(self):
        data = {
            "author": self.user.id,
            "title": "New Post",
            "content": "Some content here"
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post = serializer.save()
        self.assertEqual(post.title, "New Post")

class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.post = Post.objects.create(author=self.user, title='Post 1', content='Content here')

    def test_serialize_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content="Nice post")
        serializer = CommentSerializer(comment)
        self.assertEqual(serializer.data['content'], "Nice post")
        self.assertEqual(serializer.data['author'], self.user.id)
        self.assertEqual(serializer.data['post'], self.post.id)

    def test_create_comment(self):
        data = {
            "post": self.post.id,
            "author": self.user.id,
            "content": "Test create comment"
        }
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        comment = serializer.save()
        self.assertEqual(comment.content, "Test create comment")
