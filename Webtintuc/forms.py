from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post


# ==================== AUTHENTICATION FORMS ====================
class RegisterForm(UserCreationForm):
    """Form đăng ký tài khoản"""
    full_name = forms.CharField(
        label='Họ và tên',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Họ và tên'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    birth_date = forms.DateField(
        label='Ngày sinh',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    GENDER_CHOICES = (
        ('', '-- Chọn giới tính --'),
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    )
    gender = forms.ChoiceField(
        label='Giới tính',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Tên đăng nhập',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên đăng nhập'
        })
    )
    password1 = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu'
        })
    )

    class Meta:
        model = User
        fields = ('full_name', 'birth_date', 'gender', 'email', 'username', 'password1', 'password2')


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


# ==================== PROFILE FORM ====================
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'bio', 'birth_date', 'phone', 'gender')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Giới thiệu bản thân...'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
