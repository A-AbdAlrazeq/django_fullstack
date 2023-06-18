
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('create_course', views.create_course),
    path('view_remove/<int:id>', views.view_remove),
    path('remove_course/<int:id>', views.remove_course),
    path('addComment', views.addComment),
    path('comment/<int:id>', views.comment),
]
