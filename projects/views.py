from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def index(request):
  title = "welcome"
  return render(request,'index.html' ,{'title':title})
