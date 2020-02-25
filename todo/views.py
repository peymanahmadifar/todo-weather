import requests

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import City, Todo
from .forms import CityForm, TodoForm, newTodoForm


class IndexView(TemplateView):
    # template_name = "index.html"

    def get(self, request, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=fa&APPID=935af3b78d7590882d610d41a0c91128'
        # city = 'Tehran'

        form = CityForm()

        cities = City.objects.all()

        weather_data = []

        for city in cities:
            r = requests.get(url.format(city)).json()
            if r['cod'] == 200:
                city_weather = {
                    'id': city.id,
                    'city': r['name'],
                    'temperature': r['main']['temp'],
                    'description': r['weather'][0]['description'],
                    'icon': r['weather'][0]['icon']
                }
                weather_data.append(city_weather)

        todo_list = Todo.objects.order_by('id')
        # form = TodoForm()
        mydate = timezone.now()
        newtodoform = newTodoForm()

        context = {
            'weather_data': weather_data,
            'todo_list': todo_list,
            'cityForm': form,
            'mydate': mydate,
            'todoForm': newtodoform,
        }
        return render(request, 'index.html', context=context)


def removeCity(request, city_id):
    city = City.objects.get(pk=city_id)
    city.delete()
    return redirect('index')


@require_POST
def addCity(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=fa&APPID=935af3b78d7590882d610d41a0c91128'
    err_msg = ''
    form = CityForm(request.POST)

    if form.is_valid():
        new_city = form.cleaned_data['name']
        existing_city_count = City.objects.filter(name=new_city).count()

        if existing_city_count == 0:
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
                form.save()
            else:
                err_msg = 'شهر نامعتبر!'
        else:
            err_msg = 'این شهر قبلا افزوده شده است.'

        if err_msg:
            pass
            # form.errors['__all__'] = form.error_class(["error msg"])
    return redirect('index')


@require_POST
def addTodo(request):
    # form = TodoForm(request.POST)
    # newtodoform = newTodoForm(request.POST, instance=special_todo)
    # top line modify the special_todo instead of add new
    newtodoform = newTodoForm(request.POST)

    if newtodoform.is_valid():
        # new_todo = Todo(text=form.cleaned_data['text'])
        # new_todo = Todo(text=request.POST['text'])
        # new_todo.save()
        new_todo = newtodoform.save()
    return redirect('index')


def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()
    return redirect('index')


def deleteCompletedTodo(request):
    Todo.objects.filter(complete__exact=True).delete()
    return redirect('index')


def deleteAllTodo(request):
    Todo.objects.all().delete()
    return redirect('index')
