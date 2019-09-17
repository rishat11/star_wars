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


class Question(models.Model):
    orden_code = models.CharField(max_length=100)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name='answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text
