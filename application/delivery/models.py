from django.db import models

class Parcel(models.Model):
    product_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
