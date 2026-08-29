from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'title', 'description', 'academic_year', 'grade_level', 'subject', 'cover', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'مثال: ریاضی پایه دهم'}),
            'title': forms.TextInput(attrs={'placeholder': 'عنوان جایگزین (اختیاری)'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'توضیحات کلاس...'}),
            'academic_year': forms.TextInput(attrs={'placeholder': '1403-1404'}),
            'subject': forms.TextInput(attrs={'placeholder': 'مثال: ریاضی'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'name': 'نام کلاس',
            'title': 'عنوان',
            'description': 'توضیحات',
            'academic_year': 'سال تحصیلی',
            'grade_level': 'پایه تحصیلی',
            'subject': 'رشته/درس',
            'cover': 'تصویر کاور',
            'color': 'رنگ کلاس',
            'is_active': 'کلاس فعال است',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, f in self.fields.items():
            if name != 'color':
                f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})
            else:
                f.widget.attrs.update({'class': 'w-20 h-10 rounded-lg border'})

class JoinClassForm(forms.Form):
    invite_code = forms.CharField(label='کد دعوت', max_length=6, widget=forms.TextInput(attrs={'placeholder': 'مثال: A1B2C3', 'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 text-center tracking-widest uppercase focus:ring-2 focus:ring-daneh-500 outline-none'}))
