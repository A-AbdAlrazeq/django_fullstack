from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Description, Course, Comment


def index(request):
    context = {
        "all_the_courses": Course.objects.all(),
        "all_the_desc": Description.objects.all()
    }
    return render(request, "index.html", context)


def create_course(request):

    errors = Course.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_course = Course.objects.create(name=request.POST['name'])
        new_desc = Description.objects.create(
            course=new_course, description=request.POST['desc'])
        new_desc.save()

    return redirect('/')


def view_remove(request, id):
    context = {
        'course': Course.objects.get(id=id)
    }
    return render(request, "remove.html", context)


def remove_course(request, id):
    selected_course = Course.objects.get(id=id)
    selected_course.delete()
    return redirect('/')


def comment(request, id):
    course = Course.objects.get(id=id)
    context = {
        "course": course
    }
    return render(request, "comment.html", context)


def addComment(request):
    errors = Comment.objects.validator(request.POST)
    id = request.POST["id"]
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"comment/{id}")
    else:
        course = Course.objects.get(id=id)
        comment = Comment.objects.create(comment=request.POST['comm'])
        comment.save()
        course.comm.add(comment)
        messages.success(request, "Comment successfully Add")
        return redirect(f"comment/{id}")
