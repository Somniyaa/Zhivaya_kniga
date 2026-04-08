from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/event/<int:event_id>/', views.event_detail_api, name='event_detail_api'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('event/<int:event_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('api/calendar/<int:year>/<int:month>/', views.get_calendar_events, name='calendar_api'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('unsubscribe/', views.unsubscribe_newsletter, name='unsubscribe'),
]