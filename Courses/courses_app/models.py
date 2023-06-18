from django.db import models


class CourseManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors["name"] = "course name should be at least 5 characters"
        if len(postData['desc']) < 15:
            errors["desc"] = "  Course description should be at least 15 characters"

    def validator(self, postData):
        errors = {}
        if len(postData['comm']) < 5:
            errors["comm"] = "Course comment should be at least 5 characters"
        return errors


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CourseManager()


class Course(models.Model):
    name = models.CharField(max_length=255)
    comm = models.ManyToManyField(Comment, related_name="course_comm")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CourseManager()


class Description(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
