from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'color', 'max_members']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'مثال: گروه الف'}),
            'description': forms.Textarea(attrs={'rows':2, 'placeholder': 'توضیحات گروه...'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        labels = {'name': 'نام گروه', 'description': 'توضیحات', 'color': 'رنگ', 'max_members': 'حداکثر اعضا'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n,f in self.fields.items():
            if n!='color':
                f.widget.attrs.update({'class':'w-full rounded-xl border border-zinc-200 px-4 py-3 focus:ring-2 focus:ring-daneh-500 outline-none'})
            else:
                f.widget.attrs.update({'class':'w-20 h-10 rounded-lg border'})
