from django import forms
from .models import Category, Movie

class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['user', 'title', 'slug', 'content', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }










