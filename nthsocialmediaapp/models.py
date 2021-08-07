from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id,self.slug])

    def total_likes(self):
        return self.likes.count()

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    my_slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = my_slug
