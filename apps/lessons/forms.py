from django import forms
from .models import Lesson
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','description','date','lesson_date','homework','order','attachment','group']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'مثال: مثلثات - جلسه اول'}),
            'description': forms.Textarea(attrs={'rows':4, 'placeholder':'توضیحات درس...'}),
            'date': forms.DateInput(attrs={'type':'date'}),
            'lesson_date': forms.DateInput(attrs={'type':'date'}),
            'homework': forms.Textarea(attrs={'rows':2, 'placeholder':'تکالیف...'}),
        }
        labels = {'title':'عنوان','description':'توضیحات','date':'تاریخ','lesson_date':'تاریخ درس','homework':'تکالیف','order':'ترتیب','attachment':'فایل پیوست','group':'گروه (اختیاری)'}
    def __init__(self,*args, **kwargs):
        classroom = kwargs.pop('classroom', None)
        super().__init__(*args,**kwargs)
        if classroom is not None:
            from apps.groups.models import Group
            self.fields['group'].queryset = Group.objects.filter(classroom=classroom)
            self.fields['group'].required = False
        for f in self.fields.values():
            if getattr(f.widget, 'input_type', None) != 'file':
                f.widget.attrs.update({'class':'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})
            else:
                f.widget.attrs.update({'class':'w-full rounded-xl border border-zinc-200 px-4 py-2'})
