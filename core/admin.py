from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Event, Registration, Subscription


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'location', 'get_event_type', 'recurring', 'is_active']
    list_filter = ['event_type', 'recurring', 'is_active', 'date']
    search_fields = ['title', 'location', 'description']
    date_hierarchy = 'date'
    list_editable = ['is_active']
    
    def get_event_type(self, obj):
        return obj.get_type_display_ru()
    get_event_type.short_description = 'Тип мероприятия'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Время и место', {
            'fields': ('date', 'time', 'location')
        }),
        ('Регулярность', {
            'fields': ('recurring', 'schedule_text'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        is_new = not obj.pk
        super().save_model(request, obj, form, change)
        
        if is_new:
            self.send_notifications_to_all_subscribers(obj)
    
    def send_notifications_to_all_subscribers(self, event):
        """Отправка уведомлений всем подписчикам о новом мероприятии"""
        subscriptions = Subscription.objects.filter(is_active=True)
        
        if not subscriptions.exists():
            print(f"Нет активных подписчиков")
            return
        
        event_date = event.date.strftime('%d.%m.%Y') if event.date else 'Дата уточняется'
        event_time = event.time.strftime('%H:%M') if event.time else 'время уточняется'
        
        subject = f'📚 Новое мероприятие: {event.title}'
        
        # Текстовая версия для почтовых программ без HTML
        text_message = f"""
Здравствуйте!

В библиотеке появилось новое мероприятие:

{event.title}
Дата: {event_date}
Время: {event_time}
Место: {event.location}

{event.description[:200]}

Записаться: http://localhost:8000/calendar/

---
Это письмо отправлено, потому что вы подписались на уведомления.
"""
        
        # HTML версия с красивым оформлением
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            background-color: #F5FBF7;
            margin: 0;
            padding: 20px;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background: #FFFFFF;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(47, 107, 71, 0.08);
        }}
        .email-header {{
            background: linear-gradient(135deg, #2F6B47 0%, #1E4A32 100%);
            padding: 30px;
            text-align: center;
        }}
        .email-header h1 {{
            color: white;
            margin: 0;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .email-body {{
            padding: 30px;
        }}
        .event-details {{
            background: #E8F3ED;
            padding: 20px;
            border-radius: 16px;
            margin: 20px 0;
        }}
        .event-details p {{
            margin: 12px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .event-details i {{
            width: 24px;
            color: #2F6B47;
        }}
        .event-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1E4A32;
            margin-bottom: 15px;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, #2F6B47 0%, #1E4A32 100%);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 40px;
            margin-top: 20px;
            font-weight: 600;
        }}
        .footer {{
            background: #E8F3ED;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #4A6B58;
        }}
        .unsubscribe {{
            margin-top: 10px;
            font-size: 11px;
        }}
        .unsubscribe a {{
            color: #2F6B47;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>Живая книга</h1>
        </div>
        <div class="email-body">
            <h2>Новое мероприятие!</h2>
            <p>Дорогой читатель, мы рады сообщить вам о новом мероприятии в библиотеке:</p>
            
            <div class="event-details">
                <div class="event-title">{event.title}</div>
                <p><strong>Дата:</strong> {event_date}</p>
                <p><strong>Время:</strong> {event_time}</p>
                <p><strong>Место:</strong> {event.location}</p>
            </div>
            
            <p>Не пропустите интересное событие! Записывайтесь прямо сейчас.</p>
            
            <div class="unsubscribe">
                <p>Вы получили это письмо, потому что подписаны на новостную рассылку.</p>
            </div>
        </div>
        <div class="footer">
            <p>© 2026 Проект "Живая книга" для ЦБС г. Димитровграда</p>
        </div>
    </div>
</body>
</html>
"""
        
        success_count = 0
        failed_emails = []
        
        print(f"\n📧 Начинаю рассылку для '{event.title}'")
        print(f"👥 Подписчиков: {subscriptions.count()}")
        
        for sub in subscriptions:
            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[sub.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                success_count += 1
                print(f"  ✅ Отправлено на {sub.email}")
            except Exception as e:
                failed_emails.append(sub.email)
                print(f"  ❌ Ошибка на {sub.email}: {e}")
        
        print(f"\n📊 Статистика рассылки:")
        print(f"   Успешно: {success_count}")
        print(f"   Ошибок: {len(failed_emails)}")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at']
    list_filter = ['registered_at', 'event']
    search_fields = ['user__username', 'event__title']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    actions = ['send_test_email']
    
    def send_test_email(self, request, queryset):
        """Отправить тестовое письмо выбранным подписчикам"""
        event = Event.objects.filter(is_active=True).first()
        if not event:
            self.message_user(request, '❌ Нет мероприятий для тестового письма')
            return
        
        event_date = event.date.strftime('%d.%m.%Y') if event.date else 'Дата уточняется'
        event_time = event.time.strftime('%H:%M') if event.time else 'время уточняется'
        
        subject = f'📚 [ТЕСТ] Новое мероприятие: {event.title}'
        
        text_message = f"""
Здравствуйте!

Это ТЕСТОВОЕ письмо. В библиотеке появилось новое мероприятие:

{event.title}
Дата: {event_date}
Время: {event_time}
Место: {event.location}

{event.description[:200]}

Записаться: http://localhost:8000/calendar/
"""
        
        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
            background-color: #F5FBF7;
            margin: 0;
            padding: 20px;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background: #FFFFFF;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(47, 107, 71, 0.08);
        }}
        .email-header {{
            background: linear-gradient(135deg, #2F6B47 0%, #1E4A32 100%);
            padding: 30px;
            text-align: center;
        }}
        .email-header h1 {{
            color: white;
            margin: 0;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .email-body {{
            padding: 30px;
        }}
        .event-details {{
            background: #E8F3ED;
            padding: 20px;
            border-radius: 16px;
            margin: 20px 0;
        }}
        .event-title {{
            font-size: 18px;
            font-weight: bold;
            color: #1E4A32;
            margin-bottom: 15px;
        }}
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, #2F6B47 0%, #1E4A32 100%);
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 40px;
            margin-top: 20px;
            font-weight: 600;
        }}
        .test-badge {{
            background: #FFB74D;
            color: #E65100;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            display: inline-block;
            margin-bottom: 15px;
        }}
        .footer {{
            background: #E8F3ED;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #4A6B58;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>📚 Живая книга</h1>
        </div>
        <div class="email-body">
            <div style="text-align: center;">
                <div class="test-badge">🔧 ТЕСТОВОЕ ПИСЬМО</div>
            </div>
            <h2>Новое мероприятие!</h2>
            <p>Дорогой читатель, мы рады сообщить вам о новом мероприятии в библиотеке:</p>
            
            <div class="event-details">
                <div class="event-title">{event.title}</div>
                <p><strong>📅 Дата:</strong> {event_date}</p>
                <p><strong>⏰ Время:</strong> {event_time}</p>
                <p><strong>📍 Место:</strong> {event.location}</p>
                <p><strong>📖 Описание:</strong> {event.description[:200]}</p>
            </div>
            
            <p>Не пропустите интересное событие! Записывайтесь прямо сейчас.</p>
            
            <div style="text-align: center;">
                <a href="http://localhost:8000/calendar/" class="btn">Записаться</a>
            </div>
            
            <div style="margin-top: 20px; padding: 10px; background: #FFF3E0; border-radius: 12px;">
                <p style="margin: 0; font-size: 12px; color: #E65100;">
                    ⚡ Это тестовое письмо для проверки работы рассылки.
                </p>
            </div>
        </div>
        <div class="footer">
            <p>© 2026 Проект "Живая книга" для ЦБС г. Димитровграда</p>
        </div>
    </div>
</body>
</html>
"""
        
        for sub in queryset:
            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[sub.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                self.message_user(request, f'✅ Тестовое письмо отправлено на {sub.email}')
            except Exception as e:
                self.message_user(request, f'❌ Ошибка на {sub.email}: {e}')
    send_test_email.short_description = 'Отправить тестовое письмо'