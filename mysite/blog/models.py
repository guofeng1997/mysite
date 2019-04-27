from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='publish')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('publish', 'Publish'))
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique_for_date='publish_time')
    body = models.TextField()
    publish_time = models.DateTimeField(default=timezone.now())
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    objects = models.Manager()
    published = PublishManager()
    # 标签模型管理器
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.publish_time.year, self.publish_time.month,
                                                 self.publish_time.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}评论了“{}”'.format(self.name, self.post)