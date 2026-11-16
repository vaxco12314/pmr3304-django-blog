from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']
        labels = {
            'title': 'Título',
            'content': 'Conteúdo (HTML)',
            'categories': 'Categorias',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do post'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Digite o conteúdo ou tags HTML'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: 120px;'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        labels = {
            'author': 'Autor',
            'text': 'Comentário',
        }
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escreva seu comentário...'}),
        }
