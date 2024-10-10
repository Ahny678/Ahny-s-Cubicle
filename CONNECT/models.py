from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name


class Bword(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='bwords', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room,  on_delete=models.CASCADE)
    text = models.TextField()
    user= models.CharField(max_length=100000, default='userxx')
    date=models.DateTimeField(default=timezone.now, blank=True)


