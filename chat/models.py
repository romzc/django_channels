from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class AbstractBaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)


class Room(AbstractBaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    member = models.ManyToManyField(User, related_name='rooms')

    def get_absolute_url(self):
        return f"/{self.name}/"
    
    def __str__(self) -> str:
        return self.name


class Message(AbstractBaseModel):
    message = models.TextField(blank=False, max_length=400)
    room = models.ForeignKey(Room, related_name='message', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='message', null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
    