from django.db import models
import uuid

class User(models.Model):
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Admin(models.Model):
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
