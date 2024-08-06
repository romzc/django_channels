from django.db import models
from django.urls import reverse

# Create your models here.
class AbstractBaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False)


class Room(AbstractBaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)

    def get_absolute_url(self):
        return f"/chat/{self.name}/"
    