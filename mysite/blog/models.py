from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


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

    class Meta:
        ordering = ('-publish_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.publish_time.year, self.publish_time.month,
                                                 self.publish_time.day, self.slug])
