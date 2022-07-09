from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('skills_detail', kwargs={'pk': self.id})


class Monster(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    skills = models.ManyToManyField(Skill)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'monster_id': self.id})


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
