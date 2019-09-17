from django import forms
from .models import Recruit, Answer


class RecruitForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = ['name', 'planet', 'age', 'email']

