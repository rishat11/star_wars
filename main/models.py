from django.db import models
from django.core.validators import MinValueValidator


class Planet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sith(models.Model):
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Recruit(models.Model):
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planet, null=True, on_delete=models.SET_NULL)
    age = models.IntegerField(validators=[MinValueValidator(1)])
    email = models.EmailField()
    sith_hand_of_shadow = models.ManyToManyField(Sith, related_name='hand_of_shadow')

    def __str__(self):
        return self.name


class HandOfShadowTask(models.Model):
    orden_code = models.CharField(max_length=100)
    list_of_questions = models.TextField()

    def __str__(self):
        return self.orden_code


class TaskResult(models.Model):
    recruit = models.OneToOneField(Recruit, on_delete=models.CASCADE, related_name='result')
    list_of_questions = models.TextField()
    list_of_answers = models.TextField()

