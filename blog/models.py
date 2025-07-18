from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post_header = models.CharField(max_length=30)
    post_text = models.TextField()
    post_date = models.DateField(default=date.today)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_header