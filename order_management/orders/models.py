from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



class Orders(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    orderer = models.ForeignKey(User, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(User, related_name='favourite', blank=True )
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('orders-detail', kwargs={'pk': self.pk})