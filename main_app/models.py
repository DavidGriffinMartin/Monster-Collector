from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Monster(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # skills = models.ManyToManyField(Skill)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def fed_for_today(self):
    #     return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})