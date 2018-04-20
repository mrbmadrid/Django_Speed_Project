# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if not postData['name'].isalpha():
        	errors['name'] = "Name must only be upper and lower case letters."
   		try:
   			validate_email(postData['email'])
   		except ValidationError:
   			errors['email'] = postData['email'] + " is not a valid email."
   		if not postData['password'] == postData['confirm']:
   			errors['password_mismatch'] = "Passwords do not match."
   		if len(postData['password']) < 8:
   			errors['password_length'] = "Password must be greater than 8 characters in length."
		if len(postData['password']) > 16:
   			errors['password_length'] = "Password must be no more than 16 characters in length."
        return errors

class User(models.Model):
	name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50, unique=True)
	email = models.CharField(max_length = 255, unique=True)
	salt = models.CharField(max_length=255)
	pw = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = UserManager()

class Author(models.Model):
	name = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Author, related_name="books")
	created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
	content = models.TextField(default = "Empty")
	book = models.ForeignKey(Book, related_name="reviews")
	user = models.ForeignKey(User, related_name="reviews")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
	value = models.IntegerField(default = 5)
	book = models.ForeignKey(Book, related_name="ratings")
	user = models.ForeignKey(User, related_name="ratings")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
