from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Event, Registration
from datetime import date, timedelta

def index(request):
    today = date.today()
    
    # Получаем все активные мероприятия
    events = Event.objects.filter(is_active=True)
    
    events_data = []
    for event in events:
        # Для регулярных мероприятий - показываем следующую дату
        if event.recurring:
            next_date = event.get_next_date()
            # Если следующая дата существует, показываем мероприятие
            if next_date:
                events_data.append({
                    'id': event.id,
                    'title': event.title,
                    'date': next_date,
                    'time': event.time.strftime('%H:%M') if event.time else 'время уточняется',
                    'location': event.location,
                    'description': event.description,
                    'schedule': event.schedule_text or 'Регулярное мероприятие',
                    'event_type': event.event_type,
                    'is_registered': request.user.is_authenticated and Registration.objects.filter(
                        user=request.user, event=event
                    ).exists()
                })
        else:
            # Для разовых мероприятий - показываем только если дата не в прошлом
            if event.date and event.date >= today:
                events_data.append({
                    'id': event.id,
                    'title': event.title,
                    'date': event.date,
                    'time': event.time.strftime('%H:%M') if event.time else 'время уточняется',
                    'location': event.location,
                    'description': event.description,
                    'schedule': event.schedule_text or 'Разовое мероприятие',
                    'event_type': event.event_type,
                    'is_registered': request.user.is_authenticated and Registration.objects.filter(
                        user=request.user, event=event
                    ).exists()
                })
            # Если дата в прошлом - пропускаем (не добавляем на главную)
    
    # Сортируем по дате (ближайшие сначала)
    events_data.sort(key=lambda x: x['date'] if x['date'] else date.max)
    
    return render(request, 'core/index.html', {'events': events_data, 'today': today})


def about(request):
    return render(request, 'core/about.html')


def calendar_view(request):
    return render(request, 'core/calendar.html')


def event_detail_api(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return JsonResponse({
        'id': event.id,
        'title': event.title,
        'date': event.date.strftime('%d.%m.%Y') if event.date else 'Дата уточняется',
        'time': event.time.strftime('%H:%M') if event.time else 'время уточняется',
        'location': event.location,
        'description': event.description,
        'event_type': event.get_type_display_ru(),
        'schedule': event.schedule_text or ('Регулярное мероприятие' if event.recurring else 'Разовое мероприятие'),
        'recurring': event.recurring,
    })


@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        registration, created = Registration.objects.get_or_create(
            user=request.user,
            event=event
        )
        if created:
            messages.success(request, f'Вы успешно записаны на "{event.title}"')
        else:
            messages.warning(request, f'Вы уже записаны на "{event.title}"')
    
    return redirect('index')


@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Registration.objects.filter(user=request.user, event=event).delete()
    messages.success(request, f'Вы отменили запись на "{event.title}"')
    return redirect('profile')


def get_calendar_events(request, year, month):
    events = Event.objects.filter(is_active=True)
    events_data = []
    
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    days_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2,
        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        
        day_events = []
        for event in events:
            if not event.recurring and event.date == current_date:
                # Разовые мероприятия показываем только в дату проведения
                day_events.append({
                    'id': event.id,
                    'title': event.title,
                    'date': date_str,
                    'time': event.time.strftime('%H:%M') if event.time else None,
                    'location': event.location,
                })
            elif event.recurring and event.date and current_date >= event.date:
                # Регулярные мероприятия показываем со стартовой даты
                target_day = days_map.get(event.recurring, -1)
                if target_day == current_date.weekday():
                    day_events.append({
                        'id': event.id,
                        'title': event.title,
                        'date': date_str,
                        'time': event.time.strftime('%H:%M') if event.time else None,
                        'location': event.location,
                    })
        
        events_data.extend(day_events)
        current_date += timedelta(days=1)
    
    return JsonResponse(events_data, safe=False)


def subscribe_newsletter(request):
    """Подписка на рассылку"""
    from .models import Subscription
    from django.core.mail import send_mail
    from django.conf import settings
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                # Отправка приветственного письма
                try:
                    subject = 'Добро пожаловать в рассылку "Живая книга"!'
                    html_message = f"""
                    <!DOCTYPE html>
                    <html>
                    <head><meta charset="UTF-8"></head>
                    <body>
                        <h2>Здравствуйте!</h2>
                        <p>Вы успешно подписались на новостную рассылку проекта <strong>«Живая книга»</strong>.</p>
                        <p>Теперь вы будете первыми узнавать о новых мероприятиях в библиотеках г. Димитровграда.</p>
                        <p>Спасибо, что с нами!</p>
                        <hr>
                        <p style="font-size: 12px; color: #666;">© 2026 Проект "Живая книга"</p>
                    </body>
                    </html>
                    """
                    
                    send_mail(
                        subject,
                        '',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=html_message,
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"Ошибка отправки приветственного письма: {e}")
                
                messages.success(request, 'Вы успешно подписались на рассылку!')
            else:
                messages.info(request, 'Вы уже подписаны на рассылку')
        else:
            messages.error(request, 'Введите корректный email')
    
    return redirect('index')


def unsubscribe_newsletter(request):
    """Отписка от рассылки"""
    from .models import Subscription
    
    email = request.GET.get('email')
    if email:
        Subscription.objects.filter(email=email).delete()
        messages.success(request, 'Вы успешно отписались от рассылки')
    return redirect('index')