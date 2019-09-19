from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def register_user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be longer than 2 letters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be longer than 2 letters"
        if not EMAIL_REGEX.match(postData['reg_email']):
            errors['email'] = 'Invalid email format'
        if len(postData['new_password']) < 8 or postData['new_password'] != postData['confirm_password']:
            errors['new_password'] = 'Invalid password'
        return errors
    
    def login_user_validator(self, postData):
        login_errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            login_errors['email'] = 'Invalid email format'
        if len(postData['user_password']) < 8:
            login_errors['password'] = 'Invalid password'
        return login_errors

class User(models.Model):
    first_name = models.TextField(max_length=255)
    last_name = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    password = models.TextField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user_id = models.ForeignKey(User, related_name='user_post')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
    comment = models.TextField()
    user_id = models.ForeignKey(User, related_name='user_comment')
    message_id = models.ForeignKey(Message, related_name = "comment_to_message")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)