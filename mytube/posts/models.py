from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.urls import reverse

# Like in django docs https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#referencing-the-user-model
User = get_user_model()


class Group(models.Model):
    """Communities for sending posts"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return ' '.join([self.title, '-', self.description])


class Post(models.Model):
    """Model for bloggers posts."""
    text = models.TextField(blank=True)
    pub_date = models.DateTimeField("date_published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'posts')
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'posts',
                                blank = True, null = True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_id": self.pk, "username": self.author.username})
    
    
class Comments(models.Model):
    """Модель для комментариев"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'comments')
    text = models.TextField(blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, related_name= 'post_comments')
    created = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
