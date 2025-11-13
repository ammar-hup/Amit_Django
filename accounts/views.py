from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate, get_user_model
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    context = {
        'form': form,
        'title': 'Sign Up',
    }
    return render(request, 'registration/signup.html', context)

