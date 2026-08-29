from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title','lesson','group','description','date','exam_date','total_score','exam_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'مثال: کوییز فصل اول'}),
            'description': forms.Textarea(attrs={'rows':3}),
            'date': forms.DateInput(attrs={'type':'date'}),
            'exam_date': forms.DateInput(attrs={'type':'date'}),
        }
        labels = {'title':'عنوان','lesson':'درس مرتبط','group':'گروه (اختیاری)','description':'توضیحات','date':'تاریخ','exam_date':'تاریخ آزمون','total_score':'نمره کل','exam_type':'نوع آزمون'}
    def __init__(self,*args,**kwargs):
        classroom = kwargs.pop('classroom', None)
        super().__init__(*args,**kwargs)
        if classroom:
            self.fields['lesson'].queryset = classroom.lessons.all()
            self.fields['lesson'].required = False
            self.fields['group'].queryset = classroom.groups.all()
            self.fields['group'].required = False
        for f in self.fields.values():
            f.widget.attrs.update({'class':'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})

    def clean_total_score(self):
        v = self.cleaned_data.get('total_score')
        if v is not None and v <= 0:
            raise forms.ValidationError('حداکثر نمره باید بزرگتر از صفر باشد.')
        if v is not None and v > 100:
            raise forms.ValidationError('حداکثر نمره نمی‌تواند بیشتر از 100 باشد.')
        return v
