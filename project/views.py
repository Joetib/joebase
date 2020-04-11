from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from . import forms

def index(request):
    return render(request, 'project/index.html',{})

@login_required
def create_project(request):
    if request.method == "POST":
        project_form  = forms.ProjectCreateForm(request.data)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, f"Project {projec.name} created successfully")
        else:
            messages.error(request, f"Error with form entry")
    project_form = forms.ProjectCreateForm()
    return render(request, "project/create_project.html", {'project_form': project_form})