from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('removeCity/<city_id>', views.removeCity, name='removeCity'),
    path('addCity/', views.addCity, name='addCity'),
    path('addTodo', views.addTodo, name='addTodo'),
    path('completeTodo/<todo_id>', views.completeTodo, name='completeTodo'),
    path('deleteCompletedTodo', views.deleteCompletedTodo, name='deleteCompletedTodo'),
    path('deleteAllTodo', views.deleteAllTodo, name='deleteAllTodo'),
]
