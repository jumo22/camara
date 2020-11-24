from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    # url(r'^index/$', views.index, name='index'),
    # url(r'^$', views.CalendarView.as_view(), name='calendar'),
    # url(r'^event/new/$', views.event, name='event_new'),
    # url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='edit-event'),
    # path('index/', views.index, name='index'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/new/', views.EventCreateView.as_view(), name='new-event'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('create-reminder/', views.ReminderCreateView.as_view(), name='create-reminder'),
    path('reminders/', views.index, name='index'),
    path('my-events/', views.UserEventView.as_view(), name='user-events'),
    path('send-reminder/', views.send_reminder, name='send-reminder'),

]
