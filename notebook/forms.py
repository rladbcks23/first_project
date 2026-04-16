from django import forms
from .models import Notebook


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '노트북 이름을 입력하세요'
            }),
        }
