from django.shortcuts import render, redirect
from .models import User, Place, Comment
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "home.html")


def view_register(request):
    return render(request, "register.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/view_register')
    else:
        name = request.POST['name']
        email = request.POST['email']
        city = request.POST['city']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(name=name,
                            email=email, city=city, password=pw_hash)
        messages.success(
            request, 'User Register successfully.')
    return redirect("/view_register")


def view_login(request):
    return render(request, "login.html")


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/view_login')
        else:

            user = User.objects.filter(email=request.POST['email2'])

            if user:
                log_user = user[0]

                if bcrypt.checkpw(request.POST['password2'].encode(), log_user.password.encode()) and log_user.is_admin == True:
                    request.session['user_id'] = log_user.id
                    return redirect('/admin')
                else:
                    request.session['user_id'] = log_user.id
                    request.session['user_city'] = log_user.city
                    return redirect(f"/user/{log_user.city}")
            messages.error(request, "Email or password are invalid")

    return redirect('/view_login')


def admin(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])

        context = {
            'logged_user_info': user,
            'all_the_places':  Place.objects.all()
        }
    return render(request, "admin.html", context)


def view_create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])

        context = {
            'user': user,
        }
    return render(request, "create.html", context)


def create_place(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors = Place.objects.create_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/view_create')
            else:
                name = request.POST.get('name')
                city = request.POST.get('city')
                address = request.POST.get('address')
                new_place = Place.objects.create(name=name, city=city,
                                                 address=address)
                new_place.save()
        return redirect('/admin')


def view_edit(request, id):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "this_place": Place.objects.get(id=id),
        }
    return render(request, "update.html", context)


def update_Place(request, id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors = Place.objects.update_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/view_edit/{id}')
            else:
                this_Place = Place.objects.get(id=id)
                this_Place.name = request.POST['name']
                this_Place.city = request.POST['city']
                this_Place.address = request.POST['address']
                this_Place.save()
                messages.success(
                    request, f'{this_Place.name} information updated successfully.')
    return redirect('/admin')


def delete_Place(request, id):
    this_book = Place.objects.get(id=id)
    this_book.delete()
    return redirect('/admin')


def user(request, city):
    request.session['flag'] = True
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "this_places": Place.objects.filter(city=city),
            "city": city
        }
    return render(request, "user.html", context)


def add_to_favorites(request, place_id):
    this_Place = Place.objects.get(id=place_id)
    request.session['user_city'] = this_Place.city
    city = request.session['user_city']
    this_Place.liked_places.add(
        User.objects.get(id=request.session['user_id']))
    return redirect(f'/user/{city}')


def remove_from_favorites(request, place_id):
    flag = request.session['flag']
    this_Place = Place.objects.get(id=place_id)
    request.session['user_city'] = this_Place.city
    city = request.session['user_city']
    this_Place.liked_places.remove(
        User.objects.get(id=request.session['user_id']))
    if flag == True:
        return redirect(f'/user/{city}')
    else:
        return redirect('/my_favorites')


def show_favorites(request):
    request.session['flag'] = False
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
        }
        return render(request, "favorites.html", context)


def addComment(request, user_id, place_id):
    this_Place = Place.objects.get(id=place_id)
    request.session['user_city'] = this_Place.city
    city = request.session['user_city']
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/user/{city}')
    else:
        request.session['user_city'] = this_Place.city
        city = request.session['user_city']
        user = User.objects.get(id=user_id)
        new_comment = Comment.objects.create(
            comment=request.POST['comm'])
        new_comment.save()
        new_comment.User.add(user)
        this_Place.comment.add(new_comment)
        messages.success(request, "Comment successfully Add")
        return redirect(f'/user/{city}')


def logout(request):
    del request.session['user_id']
    return redirect('/')
