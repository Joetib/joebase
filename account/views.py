from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
User = get_user_model
# Create your views here.

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("account:login")
        else:
            messages.error(request, "Some form inputs were invalid")
    user_form = UserCreationForm()
    return render(request, "registration/register.html", {'user_form': user_form})

@login_required
def dashboard(request):
    recent_projects = request.user.projects.all()[:10]
    return render(request, 'account/dashboard.html', {'recent_projects': recent_projects})