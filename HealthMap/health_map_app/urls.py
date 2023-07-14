from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('view_register', views.view_register),
    path('register', views.register),
    path('login', views.login),
    path('view_login', views.view_login),
    path('admin', views.admin),
    path('view_create', views.view_create),
    path('create', views.create_place),
    path('view_edit/<int:id>', views.view_edit),
    path('edit/<int:id>', views.update_Place),
    path('delete/<int:id>', views.delete_Place),
    path('user/<city>', views.user),
    path('add_favorite/<int:place_id>', views.add_to_favorites),
    path('remove_favorite/<int:place_id>', views.remove_from_favorites),
    path('my_favorites', views.show_favorites),
    path('addComment/<int:user_id>/<int:place_id>', views.addComment),
    path('logout', views.logout)
]
