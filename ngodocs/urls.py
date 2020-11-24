from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('about/', views.ngoabout, name='ngo-about'),
    path('documents/', views.NGODocumentListView.as_view(), name='ngo-documents'),
    path('materials/', views.MaterialsListView.as_view(), name='ngo-materials'),
    path('my-docs/', views.UserDocsView.as_view(), name='user-docs'),
    path('document/new/', views.NGODocCreateView.as_view(), name='document-create'),
    path('document/<int:pk>/', views.NGODocDetailView.as_view(), name='document-detail'),
    path('document/<int:pk>/update/', views.NGODocUpdateView.as_view(), name='document-update'),
    path('document/<int:pk>/delete/', views.NGODocDeleteView.as_view(), name='document-delete'),

]