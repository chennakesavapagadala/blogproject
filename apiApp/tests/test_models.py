from django.test import TestCase
from django.contrib.auth.models import User
from postApp.models import Post  
from commentApp.models import Comment
from django.core.files.uploadedfile import SimpleUploadedFile

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_post_with_required_fields(self):
        post = Post.objects.create(
            author=self.user,
            title="Test Title",
            content="Test Content"
        )
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.author.username, "testuser")
        self.assertIsNone(post.image)
        self.assertIsNone(post.video)

    def test_create_post_with_image_and_video(self):
        image = SimpleUploadedFile("test.jpg", b"fake_image_content", content_type="image/jpeg")
        video = SimpleUploadedFile("test.mp4", b"fake_video_content", content_type="video/mp4")
        
        post = Post.objects.create(
            author=self.user,
            title="Multimedia Post",
            content="Has image and video",
            image=image,
            video=video
        )

        self.assertIsNotNone(post.image)
        self.assertIsNotNone(post.video)

    def test_str_method(self):
        post = Post.objects.create(
            author=self.user,
            title="Readable Title",
            content="Doesn't matter"
        )
        self.assertEqual(str(post), "Readable Title")

# Testing for Comment Model
class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.post = Post.objects.create(
            author=self.user,
            title="Sample Post",
            content="This is a post content"
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment"
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author.username, 'testuser')
        self.assertEqual(comment.content, "This is a test comment")
        self.assertIsNotNone(comment.created_at)

    def test_str_method(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment"
        )
        self.assertIn('testuser', str(comment))
        self.assertIn('This is a test', str(comment))
