from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class BlogAuthor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, help_text="Enter your bio details here.")

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        return self.user.username

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE)
    content = models.TextField(help_text="Write your blog content here.")
    post_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        ordering = ['-post_date']

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, help_text="Enter comment about blog here.")
    post_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        return self.description[:75]
