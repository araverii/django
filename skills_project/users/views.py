from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm

# Views a page where the user can register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('tw-panel')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Views a page where the user can update their profile
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('tw-panel')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
    'u_form' : u_form
    }
    return render(request, 'users/profile.html', context)


