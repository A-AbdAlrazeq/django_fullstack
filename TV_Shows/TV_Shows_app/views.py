from django.shortcuts import render, redirect, HttpResponse
from .models import Show
from django.contrib import messages


def index(request):
    context = {
        "all_the_shows": Show.objects.all()
    }
    return render(request, "shows.html", context)


def create_Show(request):

    errors = Show.objects.create_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/view_create_show')
    else:
        newShow = Show.objects.create(title=request.POST['title'], Network=request.POST['network'],
                                      release_date=request.POST['date'], description=request.POST['desc'])
        newShow.save()
    return redirect(f'view_show/{newShow.id}')


def view_create(request):

    return render(request, "index.html")


def view_show(request, id):
    show = Show.objects.get(id=id)
    date = show.release_date
    context = {
        'show': show,
        'date': date
    }
    return render(request, 'show_details.html', context)


def delete_Show(request, id):
    selected_show = Show.objects.get(id=id)
    selected_show.delete()
    return redirect('/')


def view_edit(request, id):
    context = {
        'show': Show.objects.get(id=id)
    }

    return render(request, "edit_show.html", context)


def edit_Show(request, id):

    errors = Show.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_edit/{id}')
    else:
        selected_show = Show.objects.get(id=id)
        selected_show.title = request.POST['title']
        selected_show.Network = request.POST['network']
        selected_show.release_date = request.POST['date']
        selected_show.description = request.POST['desc']
        selected_show.save()
    return redirect(f'/view_show/{selected_show.id}')
