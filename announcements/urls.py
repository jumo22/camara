from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserAnnouncementView,
    NewsListView,
)
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('announcements/', PostListView.as_view(), name='announcements-home'),
    path('announcement/<int:pk>/', PostDetailView.as_view(), name='announcement-detail'),
    path('announcement/new/', PostCreateView.as_view(), name='announcement-create'),
    path('announcement/<int:pk>/update/', PostUpdateView.as_view(), name='announcement-update'),
    path('announcement/<int:pk>/delete/', PostDeleteView.as_view(), name='announcement-delete'),
    path('about/', views.about, name='announcements-about'),
    path('search/', views.search, name='search'),
    path('my-announcements/', UserAnnouncementView.as_view(), name='user-announcements'),
    path('news/', NewsListView.as_view(), name='news'),

]