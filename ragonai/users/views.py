from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm, LoginForm, FileUploadForm
from django.contrib.auth.decorators import login_required
from .models import UserFile

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')  # Use email as username
            user.save()
            messages.success(request, 'Signup successful!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'users/profile.html', {'username': request.user.username})
    else:
        return redirect('login')


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user  # Associate the file with the logged-in user
            user_file.save()
            return redirect('file_list')  # Redirect to a list of uploaded files
    else:
        form = FileUploadForm()
    return render(request, 'users/upload_file.html', {'form': form})

@login_required
def file_list(request):
    files = UserFile.objects.filter(user=request.user)  # Get files uploaded by the user
    return render(request, 'users/file_list.html', {'files': files})
