from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, "index.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=fname, last_name=lname,
                            email=email, password=pw_hash)
        messages.success(
            request, 'User Register successfully.')
    return redirect("/")


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:

            user = User.objects.filter(email=request.POST['email2'])

            if user:
                log_user = user[0]

                if bcrypt.checkpw(request.POST['password2'].encode(), log_user.password.encode()):
                    request.session['user_id'] = log_user.id
                    messages.success(
                        request, "You have successfully logged in!")
                    return redirect('/success')
            messages.error(request, "Email or password are invalid")

    return redirect('/')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])

        context = {
            'logged_user_info': user,
            "books": Book.objects.all(),
        }
    return render(request, "success.html", context)


def create_book(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors = Book.objects.validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            else:
                title = request.POST.get('title')
                desc = request.POST.get('desc')
                uploaded_by = User.objects.get(id=user_id)
                new_book = Book.objects.create(title=title, desc=desc,
                                               uploaded_by=uploaded_by)
                new_book.save()
                book = Book.objects.get(id=new_book.id)
                book.books.add(User.objects.get(id=request.session['user_id']))
        return redirect('/success')


def show_book(request, book_id):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "this_book": Book.objects.get(id=book_id),
        }
        return render(request, "view.html", context)


def update_book(request, book_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            errors = Book.objects.update_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            else:
                this_book = Book.objects.get(id=book_id)
                this_book.title = request.POST['title']
                this_book.desc = request.POST['desc']
                this_book.save()
                messages.success(
                    request, 'Book information updated successfully.')
    return redirect(f'/view_book/{book_id}')


def delete_book(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_book.delete()
    return redirect('/success')


def add_to_favorites(request, book_id):
    book = Book.objects.get(id=book_id)
    book.books.add(User.objects.get(id=request.session['user_id']))
    return redirect(f'/view_book/{book_id}')


def remove_from_favorites(request, book_id):
    book = Book.objects.get(id=book_id)
    book.books.remove(User.objects.get(id=request.session['user_id']))
    return redirect(f'/view_book/{book_id}')


def show_favorites(request):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
        }
        return render(request, "favorites.html", context)


def logout(request):
    del request.session['user_id']
    return redirect('/')
