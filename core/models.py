from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

class Event(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Понедельник'),
        ('tuesday', 'Вторник'),
        ('wednesday', 'Среда'),
        ('thursday', 'Четверг'),
        ('friday', 'Пятница'),
        ('saturday', 'Суббота'),
        ('sunday', 'Воскресенье'),
    ]
    
    TYPE_CHOICES = [
        ('club', 'Клуб по интересам'),
        ('theatre', 'Театральный кружок'),
        ('craft', 'Творческая мастерская'),
        ('masterclass', 'Мастер-класс'),
        ('art', 'Художественная студия'),
        ('lecture', 'Лекция'),
        ('meeting', 'Встреча'),
    ]
    
    title = models.CharField('Название', max_length=200)
    date = models.DateField('Дата проведения', blank=True, null=True)
    time = models.TimeField('Время проведения', blank=True, null=True)
    location = models.CharField('Место проведения', max_length=300)
    description = models.TextField('Описание')
    schedule_text = models.CharField('Расписание', max_length=200, blank=True)
    event_type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES, default='club')
    recurring = models.CharField('Регулярность', max_length=20, choices=DAYS_OF_WEEK, blank=True)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField('Изображение', upload_to='events/', blank=True, null=True)
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
    
    def __str__(self):
        return self.title
    
    def get_type_display_ru(self):
        types = {
            'club': 'Клуб по интересам',
            'theatre': 'Театральный кружок',
            'craft': 'Творческая мастерская',
            'masterclass': 'Мастер-класс',
            'art': 'Художественная студия',
            'lecture': 'Лекция',
            'meeting': 'Встреча',
        }
        return types.get(self.event_type, 'Мероприятие')
    
    def get_next_date(self):
        """Возвращает следующую дату для регулярного мероприятия"""
        if not self.recurring or not self.date:
            return self.date
        
        today = date.today()
        if self.date >= today:
            return self.date
        
        days_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        target_day = days_map.get(self.recurring, 0)
        current_date = today
        
        while current_date.weekday() != target_day:
            current_date += timedelta(days=1)
        
        return current_date
    
    def is_past(self):
        """Проверяет, прошло ли мероприятие"""
        if self.recurring:
            # Для регулярных мероприятий всегда актуальны
            return False
        
        if not self.date:
            return False
        
        return self.date < date.today()


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Мероприятие')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'event']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
    
    def __str__(self):
        return f'{self.user.username} - {self.event.title}'


class Subscription(models.Model):
    email = models.EmailField('Email', unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str__(self):
        return self.email