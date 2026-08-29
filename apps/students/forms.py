from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_code', 'phone', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'student_code': forms.TextInput(attrs={'placeholder': 'مثال: 1403001'}),
            'phone': forms.TextInput(attrs={'placeholder': '09123456789'}),
            'notes': forms.Textarea(attrs={'rows':2, 'placeholder': 'یادداشت...'}),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'student_code': 'کد دانش‌آموزی',
            'phone': 'شماره موبایل',
            'notes': 'یادداشت',
        }

    def __init__(self, *args, classroom=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.classroom = classroom
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})

    def clean_student_code(self):
        code = self.cleaned_data.get('student_code', '').strip()
        if code and self.classroom:
            qs = Student.objects.filter(classroom=self.classroom, student_code=code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('کد دانش‌آموزی در این کلاس تکراری است.')
        return code

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not phone.startswith('09'):
            raise forms.ValidationError('شماره باید با 09 شروع شود.')
        return phone


class EnrolledStudentForm(forms.ModelForm):
    """Form for creating/editing enrolled User students within a classroom context"""
    class Meta:
        from django.contrib.auth import get_user_model
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'phone', 'student_code', 'notes']
        labels = {
            'username': 'نام کاربری',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone': 'شماره موبایل',
            'student_code': 'کد دانش‌آموزی',
            'notes': 'یادداشت',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'phone': forms.TextInput(attrs={'placeholder': '09123456789'}),
            'student_code': forms.TextInput(attrs={'placeholder': 'کد دانش‌آموزی'}),
            'notes': forms.Textarea(attrs={'rows':2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})
