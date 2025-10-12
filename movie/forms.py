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
            'poster': forms.FileInput(attrs={'class': 'form-control'}),  # Добавить класс для стилей
        }

        help_texts = {
            'poster': 'Выберите изображение для постера',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 4:
            raise forms.ValidationError('Слишком короткое название')
        if len(title) > 100:
            raise forms.ValidationError('Слишком длинное название')
        return title

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


