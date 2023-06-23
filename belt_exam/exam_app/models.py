from django.db import models
import re
import bcrypt
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or not postData['name'].isalpha():
            errors["name"] = "first name should be at least 2 chars and contains letters only"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        email = postData['email']
        taken = User.objects.filter(email=email).first()
        if taken:
            errors['email3'] = "this email is register,try another one"

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
        # errors["email3"] = "Email not found in DB"

        return errors

    def create_team(self, postData):
        errors = {}
        selected_team = Team.objects.filter(name=postData['name'])
        name = postData['name']
        skill = postData['level']
        day = postData['day']

        if len(name) < 1:
            errors["name"] = "team name cannot be empty!"
        elif len(selected_team) > 0:
            errors['name'] = " New Team is already exists. try another Team"
        if len(skill) < 1:
            errors["level"] = "skill level cannot be empty!"

        if len(day) < 1:
            errors["day"] = "game day cannot be empty!"

        return errors

    def update_team(self, postData):
        errors = {}
        name = postData['name']
        skill = postData['level']
        day = postData['day']

        if len(name) < 1:
            errors["name"] = "team name cannot be empty!"

        if len(skill) < 1:
            errors["level"] = "skill level cannot be empty!"

        if len(day) < 1 or day == "":
            errors["day"] = "game day cannot be empty!"

        return errors

    def add_player(self, postData):
        errors = {}
        name = postData['player']

        if len(name) < 1:
            errors["name"] = "player name cannot be empty!"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Team(models.Model):
    name = models.CharField(max_length=255)
    skill_level = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    game_day = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        User, related_name="teams", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Player(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name="team",
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
