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
        fields = ('name', 'file')

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('text',)