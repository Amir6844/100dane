from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
            'phone': forms.TextInput(attrs={'placeholder': '09123456789'}),
        }
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone': 'شماره موبایل',
            'role': 'نقش',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 focus:border-daneh-500 outline-none transition'})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 focus:border-daneh-500 outline-none transition'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'national_code', 'bio', 'avatar']
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'phone': 'شماره موبایل',
            'national_code': 'کد ملی',
            'bio': 'درباره من',
            'avatar': 'تصویر پروفایل',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if name != 'avatar':
                f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})
