from django.db import models

class Restaurant(models.Model):
    name = models.TextField(max_length=64)
    opens_at = models.TimeField()
    closes_at = models.TimeField()