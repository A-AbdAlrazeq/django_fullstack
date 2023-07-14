from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or not postData['name'].isalpha():
            errors["name"] = "Username should be at least 2 chars and contains letters only"
        email = postData['email']
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email address!"
        if len(email) < 1:
            errors["email"] = "Email cannot be empty!"
        taken = User.objects.filter(email=email).first()
        if taken:
            errors['email'] = "this email is register,try another one"
        if len(postData['city']) < 1:
            errors["city"] = "You Should Select a City"

        if len(postData['password']) < 8:
            errors['password'] = "The password must be 8 characters minimum"
        if postData['password'] != postData['pwdconfirm']:
            errors['password'] = "Passwords are note the same"

        return errors

    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        email2 = postData['email2']
        password2 = postData['password2']
        usr = User.objects.filter(email=email2).first()
        if len(email2) < 1:
            errors["email2"] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(email2):
            errors["email2"] = "Invalid Email Address!"
        if len(password2) < 1:
            errors["password2"] = "Password cannot be empty!"
        if usr and password2:
            if not bcrypt.checkpw(password2.encode(), usr.password.encode()):
                errors["password2"] = "Incorrect password. Try again!"

        return errors

    def create_validator(self, postData):
        errors2 = {}
        this_Place = Place.objects.filter(name=postData['name'])
        if len(postData['name']) < 5:
            errors2["name"] = "The name should be at least 5 characters"
        if len(this_Place) > 0:
            errors2['name'] = " This Place is already exists. try another Place"
        if len(postData['city']) < 4:
            errors2["city"] = "You Should Select a City"

        if len(postData['address']) < 5:
            errors2["address"] = "The address should be at least 5 characters"
        return errors2

    def update_validator(self, postData):
        errors2 = {}
        if len(postData['name']) < 5:
            errors2["name"] = "The name should be at least 5 characters"
        if len(postData['city']) < 4:
            errors2["city"] = "You Should Select a City"

        if len(postData['address']) < 5:
            errors2["address"] = "The address should be at least 5 characters"
        return errors2

    def comment_validator(self, postData):
        errors3 = {}
        if len(postData['comm']) < 5:
            errors3["comm"] = "comment should be at least 5 characters"
        return errors3


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Comment(models.Model):
    comment = models.TextField()
    User = models.ManyToManyField(User, related_name="user_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Place(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    liked_places = models.ManyToManyField(User, related_name="liked_places")
    comment = models.ManyToManyField(Comment, related_name="places_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
