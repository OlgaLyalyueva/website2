from .models import Post, Comment, User, Avatar
from django import forms
from django_registration import forms as reg_forms
from django.contrib.auth.views import PasswordResetView


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date', 'user', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('published_date', 'fk_post')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class RegistrationForm(reg_forms.RegistrationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['avatar']
