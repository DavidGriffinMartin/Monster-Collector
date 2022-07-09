from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Monster
from .forms import FeedingForm


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def monsters_index(request):
    monsters = Monster.objects.all()
    return render(request, 'monsters/index.html', { 'monsters': monsters})


def monsters_detail(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    feeding_form = FeedingForm()
    return render(request, 'monsters/detail.html', {'monster': monster, 'feeding_form': feeding_form})


def add_feeding(request, monster_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.monster_id = monster_id
        new_feeding.save()
    return redirect('detail', monster_id=monster_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            user = form.save()
            login(request, user)
            return redirect('index')
        except:
            error_message = form.errors
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class MonsterCreate(LoginRequiredMixin, CreateView):
    model = Monster
    fields = ['name', 'type', 'description', 'age']
    success_url = '/monsters/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
      
      
class MonsterUpdate(LoginRequiredMixin, UpdateView):
    model = Monster
    fields = ['type', 'description', 'age']


class MonsterDelete(LoginRequiredMixin, DeleteView):
    model = Monster
    success_url = '/monsters/'