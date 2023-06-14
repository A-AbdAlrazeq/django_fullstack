
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('create_show', views.create_Show),
    path('view_create_show', views.view_create),
    path('view_show/<int:id>', views.view_show),
    path('delete_show/<int:id>', views.delete_Show),
    path('edit_show/<int:id>', views.edit_Show),
    path('view_edit/<int:id>', views.view_edit)
]
