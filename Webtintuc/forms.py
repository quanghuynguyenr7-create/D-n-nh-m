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



# ==================== POST FORMS ====================
class PostForm(forms.ModelForm):
    """Form tạo/chỉnh sửa bài viết (có ảnh tiêu đề)"""
    class Meta:
        model = Post
        fields = ('title', 'summary', 'content', 'category', 'thumbnail', 'status', 'post_type')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề bài viết'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tóm tắt ngắn gọn'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Nội dung bài viết'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
        }
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
