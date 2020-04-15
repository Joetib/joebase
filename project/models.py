from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    """
    This is the base project model. This is the main interface that holds data for every separate app or site built
    on this backend
    """
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    authentication = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<Project: {self.name}>'
    

class Table(models.Model):
    authentication_choices = (
        ('A', 'Admin Only'),
        ('B', 'Viewed and edited by authenticated Users'),
        ('C', 'Viewed only by authenticated Users'),
        ('D', 'Viewed and Edited by all'),
    )
    project = models.ForeignKey(Project, related_name="tables", on_delete=models.CASCADE)
    name=models.CharField(max_length=500)
    authentication_option = models.CharField(max_length=1, choices=authentication_choices)
    date_created = models.DateTimeField(auto_now_add=True)
    
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'<Table: {self.project.name} | {self.name}>'


class Field(models.Model):
    field_choices = (
        ('T', 'Text'),
        ('I', "Image"),
        ('F', 'File'),
    )
    required = models.BooleanField(default=False)
    name = models.CharField(max_length=500)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="fields")
    field_type  = models.CharField(choices=field_choices, max_length=1)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_created',)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Field: {self.name}>'
    
    def get_field_type(self):
        if self.field_type == 'T':
            return 'Text'
        elif self.field_type == 'F':
            return 'File'
        elif self.field_type == "I":
            return 'Image'
        return ""

    

class Entry(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="entries")

class FieldEntry(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="fieldentries")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='fieldentries')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('field',)

def get_file_upload_dir(instance, filename):
    return f"{instance.field_entry.entry.table.project.owner.username}/{instance.field_entry.entry.table.project.name}/{instance.field_entry.entry.table.name}/{filename}"

class File(models.Model):
    field_entry = models.OneToOneField(FieldEntry, related_name="file", on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_upload_dir)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Image(models.Model):
    field_entry = models.OneToOneField(FieldEntry, related_name="image", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_upload_dir)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Text(models.Model):
    field_entry = models.OneToOneField(FieldEntry, related_name="text", on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
