from django import forms
from .models import Movie

class AddMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'content', 'poster']
        labels = {
            'title': 'Название фильма',
            'content': 'Короткое описание',
            'poster': 'Постер фильма',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),  # Добавь класс для стилей
        }

        help_texts = {
            'poster': 'Выберите изображение для постера',
        }


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['poster']
        widgets = {
            'poster': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'  # Разрешаем только изображения
            }),
        }
        labels = {
            'poster': 'Новый постер фильма:',
        }


