from django import forms
from .models import Project, Table, Field, FieldEntry, File, Text

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'authentication', 'description',)

class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('authentication', 'description')

class TableCreateForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('name', 'authentication_option')


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('name', 'field_type', 'required')

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('text',)


class EntryForm(forms.Form):
    def __init__(self, entry, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        print(entry.fields.all())
        for field in entry.fields.all():
        
            if field.field_type == 'T':
                print('got here')
                self.fields[field.name]= forms.CharField(required=field.required)
            elif field.field_type == 'F':
                self.fields[field.name] = forms.FileField(required=field.required)
            elif field.field_type == 'I':
                self.fields[field.name] = forms.ImageField(required=field.required)
        
