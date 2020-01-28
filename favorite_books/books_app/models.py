from __future__ import unicode_literals
import re
from django.db import models

class LoginManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.filter(email = postData['email']):
            email_found = True
        else:
            email_found = False
        if len(postData['first_name']) < 3:
            errors['first_name'] = "Invalid: First Name must be longer than three characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Invalid: Last Name must be longer than three characters"
        if not EMAIL_REGEX.match(postData['email']) or email_found == True:
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password_length'] = "Password should be at least 8 characters"
        if not postData['password'] == postData['confirm_password']:
            errors['password_confirm'] = "Passwords should match"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required and must be unique"
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = LoginManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    creator = models.ForeignKey(User, related_name="created_books", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="favorites")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    objects = BookManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)