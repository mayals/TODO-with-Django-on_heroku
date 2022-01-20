from django import forms
from .models import Task
from django.core.exceptions import ValidationError

class AddTask(forms.ModelForm):
    T_name = forms.CharField(max_length=15,label='add task')
    
    class Meta:
        model= Task
        fields = ('T_name',)


    



class EditTask(forms.ModelForm):
    T_name = forms.CharField(max_length=15)
    
    class Meta:
        model= Task
        fields = ('T_name',)
