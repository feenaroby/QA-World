from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date



class DateInput(forms.DateInput):
    input_type = 'date'
    max=date.today()

class questionForm(ModelForm):
    class Meta:
        model = question
        fields = ['categry','question','e_date']
        widgets = {
            'e_date': DateInput(),
        }

class tbl_answer(ModelForm):
    class Meta:
        model = tbl_answer
        fields = ['pending', 'answer', 'review']
        widgets = {
            'e_date': DateInput(),
        }

