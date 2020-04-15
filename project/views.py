from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
# Create your views here.
from . import forms
from .models import Project, Table, Entry, FieldEntry, File, Text, Image

def index(request):
    return render(request, 'project/index.html',{})

@login_required
def create_project(request):
    if request.method == "POST":
        project_form  = forms.ProjectCreateForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, f"Project {project.name} created successfully")
        else:
            messages.error(request, f"Error with form entry")

    project_form = forms.ProjectCreateForm()
    return render(request, "project/create_project.html", {'project_form': project_form})

@login_required
def project_page(request, pk):
    project = get_object_or_404(Project, id=pk, owner=request.user)
    table_form = forms.TableCreateForm()
    return render(request, 'project/project_page.html', {'project': project, 'table_form': table_form})



@login_required
def table_view(request, project_pk, table_pk=None):
    project = get_object_or_404(Project, id=project_pk, owner=request.user)
    if table_pk != None:
        table = project.tables.get(id=table_pk)
        
        if table is None:
            return Http404(request)
    else:
        table = None
    if request.method == "POST":
        table_form = forms.TableCreateForm(request.POST, instance=table)
        if table_form.is_valid():
            table = table_form.save(commit=False)
            table.project = project
            table.save()
            messages.success(request, f"Table {table.name} created successfully")
        else:
            messages.error(request, "Some Form inputs were incorect")
    field_form = forms.FieldForm()
    entry_form = forms.EntryForm(table)
    return render(request,'project/table_page.html', {'table': table, 'field_form': field_form, 'entry_form': entry_form} )



@login_required
def add_field(request, project_pk, table_pk):
    table = get_object_or_404(Table, id=table_pk)
    if table.project.owner != request.user:
        return Http404(request)
    if request.method == "POST":
        field_form = forms.FieldForm(request.POST)
        if field_form.is_valid():
            field = field_form.save(commit=False)
            field.table = table
            field.save()
            messages.success(request, f"Field {field.name} created successfully")
    return redirect('project:table-view', project_pk=table.project.id, table_pk=table.id)

@login_required
def add_entry(request, project_pk, table_pk):
    table = get_object_or_404(Table, id=table_pk)
    if table.project.owner != request.user:
        return Http404(request)
    if request.method=="POST":
        entryForm = forms.EntryForm(table, data=request.POST, files=request.FILES)
        if entryForm.is_valid():
            data = entryForm.cleaned_data
            files = entryForm.files
            print(files, data, '\n\n\n')
            entry = Entry.objects.create(table=table)
            for field in table.fields.all():
                field_entry = FieldEntry.objects.create(entry=entry, field=field)
                field_entry.save()
                if field.field_type == 'F':
                    file = File.objects.create(field_entry=field_entry, file=data.get(field.name))
                    file.save()
                elif field.field_type == 'I':
                    image = Image.objects.create(field_entry=field_entry, image=data.get(field.name))
                    image.save()
                elif field.field_type== 'T':
                    text = Text.objects.create(field_entry=field_entry, text=data.get(field.name))
                    text.save()
            messages.success(request, "Entry created successfully")
        messages.error(request, "Problem creating entry")
    return redirect('project:table-view', project_pk=table.project.id, table_pk=table.id)
