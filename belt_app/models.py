from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        #characters input length error for last_name
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
            #email validation right format error    
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!" 
        #password confirmation error
        if postData['password'] != postData['confirm']:
            errors["confirm"] = "Passwords don't match"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors
            
    def basic_validator_second(self, postData):
        errors = {}
        #email validation right format error for the login form
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_login']):                
            errors['email-login'] = "Invalid email address!"
        #password length smaller than 18 characters error
        if len(postData['password_login']) < 8:
            errors["password-login"] = "Password should be at least 8 characters"
        return errors
    
class WishManager(models.Manager):
    def basic_validator_edit_wish(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"]="item should be at least 3 characters"
        if len(postData['desc']) < 3:
            errors["desc"] = "description should be at least 3 characters"
        return errors
        
    def basic_validator_new_wish(self, postData):
        errors = {}
        if len(postData['new_item']) < 3:
            errors["item"]="item should be at least 3 characters"
        if len(postData['new_desc']) < 1:
            errors["desc"] = "description must be provided"
        return errors
        
    
    
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
    
    
class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc=models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=WishManager()
    
class Granted(models.Model):
    item = models.CharField(max_length=255)
    users_granted_wishes = models.ForeignKey(User, related_name="granted_wishes",on_delete = models.CASCADE)
    granted_wishes_likes = models.ManyToManyField(User, related_name="liked_granted_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    