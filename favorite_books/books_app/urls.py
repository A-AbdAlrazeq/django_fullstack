from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('create_book', views.create_book),
    path('view_book/<int:book_id>', views.show_book),
    path('edit_book/<int:book_id>', views.update_book),
    path('delete_book/<int:book_id>', views.delete_book),
    path('add_favorite/<int:book_id>', views.add_to_favorites),
    path('remove_favorite/<int:book_id>', views.remove_from_favorites),
    path('my_favorites', views.show_favorites)


]
