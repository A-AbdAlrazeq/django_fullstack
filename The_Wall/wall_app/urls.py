from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('create_post', views.create_post),
    path('delete_message/<int:id>', views.delete_message),
    path('comment/<int:id>', views.post_comment),

]
