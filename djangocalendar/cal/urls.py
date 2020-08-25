from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('search/', views.event_search, name='search'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/add/', views.event, name='event_new'),
    path('event/edit/<int:event_id>/', views.event, name='event_edit'),
]