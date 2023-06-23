from django.shortcuts import render, redirect
from .models import User, Team, Player
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
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(name=name,
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
            'all_the_teams': Team.objects.all(),
        }
    return render(request, "success.html", context)


def view_create(request):
    if 'user_id' not in request.session:
        return redirect('/')

    return render(request, "create_team.html")


def create_team(request):
    user_id = request.session.get('user_id')
    errors = Team.objects.create_team(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/view_add')
    else:
        user = User.objects.get(id=user_id)
        newTeam = Team.objects.create(name=request.POST['name'], skill_level=request.POST['level'],
                                      game_day=request.POST['day'], uploaded_by=user)
        newTeam.save()
    return redirect('/success')


def view_team(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session.get('user_id')
        context = {
            'team': Team.objects.get(id=id),
            'user': User.objects.get(id=user_id)
        }

    return render(request, "view_team.html", context)


def view_edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'team': Team.objects.get(id=id)
    }

    return render(request, "edit_team.html", context)


def edit_team(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    errors = Team.objects.update_team(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_edit/{id}')
    else:
        selected_team = Team.objects.get(id=id)
        selected_team.name = request.POST['name']
        selected_team.skill_level = request.POST['level']
        selected_team.game_day = request.POST['day']
        selected_team.save()
    return redirect(f'/view_team/{selected_team.id}')


def add_player(request, team_id):
    errors = Player.objects.add_player(request.POST)
    selected_Team = Team.objects.get(id=team_id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_team/{team_id}')
    if selected_Team.team.count() > 8:
        messages.error(
            request, 'The team is Full')
    else:
        add_player = Player.objects.create(
            name=request.POST['player'], team=selected_Team)
        add_player.save()
    return redirect(f'/view_team/{team_id}')


def delete_team(request, id):
    selected_team = Team.objects.get(id=id)
    selected_team.delete()
    return redirect('/success')


def logout(request):
    del request.session['user_id']
    return redirect('/')
