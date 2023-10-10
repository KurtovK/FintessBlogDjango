from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post, Category, UserProfile, FitnessService
from django.utils.translation import gettext_lazy as _


class CommentsForm(forms.ModelForm):
    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['content', 'parent_comment', 'name']

    labels = {
        'content': _(''),
    }

    widgets = {
        'content': forms.TextInput(),
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentsForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['name'].initial = self.user.username
            self.fields['email'].initial = self.user.email


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='Имя пользователя', required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea, label='Текст')
    image = forms.ImageField(label='Изображение')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    description = forms.CharField(widget=forms.Textarea, label='Описание', required=False)
    first_name = forms.CharField(max_length=255, label='Имя', required=False)
    last_name = forms.CharField(max_length=255, label='Фамилия', required=False)
    email = forms.EmailField(label='Электронная почта', required=False)
    mobile_number = forms.CharField(max_length=20, label='Телефон', required=False)
    address_line1 = forms.CharField(max_length=255, label='Адрес', required=False)

    class Meta:
        model = UserProfile
        fields = ['avatar', 'description', 'first_name', 'last_name', 'email', 'mobile_number', 'address_line1']

    def save(self, commit=True):
        # Сначала сохраняем профиль пользователя
        user_profile = super().save(commit=False)
        if commit:
            user_profile.save()

        # Затем обновляем email пользователя
        user = user_profile.user
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user_profile


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название',
        }


class FitnessServiceForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all(),
                                    widget=forms.Select(
                                        attrs={'class': 'form-control form-control-lg', 'readonly': True}))

    class Meta:
        model = FitnessService
        fields = ['title', 'description', 'author', 'price', 'image', 'contact_data']

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'image': 'Изображение',
            'contact_data': 'Контактные данные',
            'author': 'Автор',
        }
