from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from core.models import Registration

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not username or not password1:
            messages.error(request, 'Заполните обязательные поля')
            return render(request, 'users/register.html')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(username=username, password=password1)
        if email:
            user.email = email
            user.save()
        
        login(request, user)
        messages.success(request, f'Добро пожаловать, {username}!')
        return redirect('profile')
    
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('index')


@login_required
def profile_view(request):
    # Получаем или создаем профиль
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    events_data = []
    for reg in registrations:
        next_date = reg.event.get_next_date()
        events_data.append({
            'id': reg.event.id,
            'title': reg.event.title,
            'date': next_date if next_date else reg.event.date,
            'time': reg.event.time.strftime('%H:%M') if reg.event.time else 'время уточняется',
            'location': reg.event.location,
            'registered_at': reg.registered_at
        })
    
    return render(request, 'users/profile.html', {
        'events': events_data,
        'profile': profile
    })


@login_required
def edit_profile_view(request):
    # Получаем или создаем профиль
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        
        if username and username != user.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
                return redirect('edit_profile')
            user.username = username
        
        user.email = email
        user.save()
        
        profile.phone = request.POST.get('phone', '')
        
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
            profile.save()
        
        profile.save()
        
        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('profile')
    
    return render(request, 'users/edit_profile.html', {'profile': profile})