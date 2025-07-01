from django.db import models
from datetime import date

# Create your models here.
class Post(models.Model):
    post_header = models.CharField(max_length=30)
    post_text = models.TextField()
    post_date = models.DateField(default=date.today)

    def __str__(self):
        return self.post_header