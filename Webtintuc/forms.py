from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post


# ==================== AUTHENTICATION FORMS ====================
class RegisterForm(UserCreationForm):
    """Form đăng ký tài khoản"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên đăng nhập'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    """Form đăng nhập"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên đăng nhập'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
    )


# ==================== COMMENT FORMS ====================
class CommentForm(forms.ModelForm):
    """Form gửi bình luận"""
    content = forms.CharField(
        label='Bình luận',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Viết bình luận của bạn...',
            'rows': 4
        })
    )

    class Meta:
        model = Comment
        fields = ('content',)
