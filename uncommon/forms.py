from django import forms
from datetime import date
from django.core.exceptions import ValidationError

def is_positive(value):
    if value <= 0:
        raise ValidationError('You broke. Stay home!')

def is_date(value):
    if value < date.today():
        raise ValidationError('From today on!')

class my_form(forms.Form):
    budget = forms.IntegerField()
    departure_date = forms.DateField()
    return_date = forms.DateField()








