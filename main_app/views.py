from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Monster, Skill, Photo
from .forms import FeedingForm

import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'catcollector-avatar-13'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def monsters_index(request):
    monsters = Monster.objects.all()
    return render(request, 'monsters/index.html', {'monsters': monsters})


@login_required
def monsters_detail(request, monster_id):
    monster = Monster.objects.get(id=monster_id)
    feeding_form = FeedingForm()
    skills_monster_doesnt_have = Skill.objects.exclude(
        id__in=monster.skills.all().values_list('id'))
    return render(request, 'monsters/detail.html', {'monster': monster, 'feeding_form': feeding_form, 'skills': skills_monster_doesnt_have})


@login_required
def add_feeding(request, monster_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.monster_id = monster_id
        new_feeding.save()
    return redirect('detail', monster_id=monster_id)


@login_required
def assoc_skill(request, monster_id, skill_id):
    Monster.objects.get(id=monster_id).skills.add(skill_id)
    return redirect('detail', monster_id=monster_id)


@login_required
def add_photo(request, monster_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, monster_id=monster_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
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


class SkillList(LoginRequiredMixin, ListView):
    model = Skill
    template_name = 'skills/index.html'


class SkillDetail(LoginRequiredMixin, DetailView):
    model = Skill
    template_name = 'skills/detail.html'


class SkillCreate(LoginRequiredMixin, CreateView):
    model = Skill
    fields = ['name']


class SkillUpdate(LoginRequiredMixin, UpdateView):
    model = Skill
    fields = ['name']


class SkillDelete(LoginRequiredMixin, DeleteView):
    model = Skill
    success_url = '/skills/'
