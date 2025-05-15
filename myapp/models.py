from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # ideally hashed — not plain text

    def __str__(self):
        return f"{self.full_name} ({self.email})"
