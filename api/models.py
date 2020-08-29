from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
