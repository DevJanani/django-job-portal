from django import forms
from .models import Job

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['company_name', 'title', 'description', 'salary', 'location']

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }