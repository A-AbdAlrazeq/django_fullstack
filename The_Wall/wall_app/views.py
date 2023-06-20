from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Comments
from django.contrib import messages
import bcrypt
from datetime import datetime, timezone


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
        print(pw_hash)
        request.session['username'] = fname + " " + lname
        request.session['status'] = "Registered"
        User.objects.create(first_name=fname, last_name=lname,
                            email=email, password=pw_hash)
    return redirect("/")


def login(request):
    errors2 = User.objects.login_validator(request.POST)
    if len(errors2) > 0:
        for key, value in errors2.items():
            messages.error(request, value)
        return redirect('/')

    users = User.objects.filter(email=request.POST['email2'])
    if users:
        logged_user = users[0]
        if bcrypt.checkpw(request.POST['password2'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
        print("""Wrong password""")
    return redirect("/")


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        all_messages = Message.objects.all()
        all_comments = Comments.objects.all()
        user = User.objects.get(id=request.session['user_id'])

        context = {
            'logged_user_info': user,
            'messages': all_messages,
            'comments': all_comments,
            'error': request.session['error']
        }
    return render(request, "success.html", context)


def logout(request):
    del request.session['user_id']
    del request.session['error']
    return redirect('/')


def create_post(request):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'])
        recent_post = Message.objects.create(
            message=request.POST['post'], user_id=current_user)
    return redirect('/success')


def post_comment(request, id):
    if request.method == 'POST':
        current_user = User.objects.get(id=request.session['user_id'])
        post_to_message = Message.objects.get(id=id)
        Comments.objects.create(
            comment=request.POST['comment'], user_id=current_user, message_id=post_to_message)
    return redirect('/success')


def delete_message(request, id):
    if request.method == 'POST':
        message_to_delete = Message.objects.get(id=id)
        current_time = datetime.now(timezone.utc)
        time_difference = current_time - message_to_delete.create_at
        if time_difference.total_seconds() <= 1800:
            request.session['error'] = ""
            message_to_delete.delete()
            return redirect('/success')
        else:
            request.session['error'] = "You can only delete Posts written within the last 30 minutes."
    return redirect('/success')
