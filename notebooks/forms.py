from django import forms
from .models import Notebook, Post


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '노트북 이름을 입력하세요'
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '포스트 이름을 입력하세요'
            }),
        }
