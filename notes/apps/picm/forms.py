from django import forms
from . import models as Models


# fix create table

try:
    file_types = Models.PicmCategory.objects.all().values_list('name')
    TYPES = []
    for t in file_types:
        TYPES.append((t[0], t[0]))
except:
    TYPES=[('test','test')]
finally:
    if not TYPES:
        TYPES = [('test', 'test')]

class Single_UploadFileForm(forms.Form):
    Type = forms.ChoiceField(widget=forms.Select, choices=TYPES)
    # File = forms.FileField()
    File = forms.ImageField()   # need module pillow
    Comment = forms.CharField(widget=forms.Textarea, required=False)


class Mult_UploadFileForm(forms.Form):
    Type = forms.ChoiceField(widget=forms.Select, choices=TYPES)
    # Files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    Files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    Comment = forms.CharField(widget=forms.Textarea, required=False)
