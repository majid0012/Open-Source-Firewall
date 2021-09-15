from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .filter import filter_packets
from .firewall import check_packet


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def header(request):
    Brand = ['A', 'T', 'I', 'B']
    Total = [2, 4, 2, 9]
    Price = [2, 9, 20, 9]

    return render(request, 'users/header.html', context={'LUnique': zip(Brand, Total, Price)})


@login_required
def home(request):
    return render(request, 'users/open.html')


@login_required
def filter(request):
    packets = filter_packets()
    return render(request, 'users/filter.html', context={'packets': packets})


@login_required
def firewall(request):
    packets = check_packet()
    return render(request, 'users/firewall.html', context={'packets': packets})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})