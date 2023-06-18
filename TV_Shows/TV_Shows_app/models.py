from django.db import models
from django.utils import timezone
from datetime import datetime


class ShowManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        tv_Show = Show.objects.filter(title=postData['title'])
        if len(postData['title']) < 2:
            errors["title"] = "title should be at least 2 characters"
        elif len(tv_Show) > 0:
            errors['title'] = " New title is already exists. try another title"

        if len(postData['network']) < 3:
            errors["network"] = " network should be at least 3 characters"

        if len(postData['desc']) > 0 and len(postData['desc']) < 10:
            errors["desc"] = " descriptions should be at list 10 characters"
        release_date_str = postData.get('date')
        if release_date_str:
            release_date = datetime.strptime(
                release_date_str, '%Y-%m-%d').date()
            current_date = timezone.now().date()
            if release_date > current_date:
                errors["date"] = "Release date must be in the past"
        return errors

    def update_validator(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors["title"] = "title should be at least 2 characters"

        if len(postData['network']) < 3:
            errors["network"] = " network should be at least 3 characters"

        if len(postData['desc']) > 0 and len(postData['desc']) < 10:
            errors["desc"] = " descriptions should be at list 10 characters"
        release_date_str = postData.get('date')
        if release_date_str:
            release_date = datetime.strptime(
                release_date_str, '%Y-%m-%d').date()
            current_date = timezone.now().date()
            if release_date > current_date:
                errors["date"] = "Release date must be in the past"
        return errors


class Show(models.Model):
    title = models.CharField(max_length=255)
    Network = models.CharField(max_length=255)
    release_date = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
