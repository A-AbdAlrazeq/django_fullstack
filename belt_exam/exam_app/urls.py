from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('view_add', views.view_create),
    path('create_team', views.create_team),
    path('view_team/<int:id>', views.view_team),
    path('view_edit/<int:id>', views.view_edit),
    path('edit_team/<int:id>', views.edit_team),
    path('delete_team/<int:id>', views.delete_team),
    path('add_player/<int:team_id>', views.add_player),
]
