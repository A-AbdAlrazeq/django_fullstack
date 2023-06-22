from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 2 or not postData['fname'].isalpha():
            errors["fname"] = "first name should be at least 2 chars and contains letters only"
        if len(postData['lname']) < 2 or not postData['fname'].isalpha():
            errors["lname"] = "last name should be at least 2 chars and contains letters only"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "The password must be 8 characters minimum"
        if postData['password'] != postData['pwdconfirm']:
            errors['password'] = "Passwords are note the same"

        return errors

    def login_validator(self, postData):
        errors = {}
        email2 = postData['email2']
        password2 = postData['password2']
        usr = User.objects.filter(email=email2).first()
        if len(email2) < 1:
            errors["email2"] = "Email cannot be empty!"
        if len(password2) < 1:
            errors["password2"] = "Password cannot be empty!"
        if usr:
            if not bcrypt.checkpw(password2.encode(), usr.password.encode()):
                errors["password2"] = "Incorrect password. Try again!"

        return errors

    def validator(self, postData):
        errors = {}
        if Book.objects.filter(title=postData['title']).exists():
            errors["title"] = "This title have been already used"
        if len(postData['title']) < 5:
            errors["title_2"] = "The title should be at least 5 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "The descriptions should be at least 10 characters"
        return errors

    def update_validator(self, postData):
        errors2 = {}
        if len(postData['title']) < 5:
            errors2["title_2"] = "The title should be at least 5 characters"
        if len(postData['desc']) < 10:
            errors2["desc"] = "The descriptions should be at least 10 characters"
        return errors2


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(
        User, related_name="books", on_delete=models.CASCADE)
    books = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
