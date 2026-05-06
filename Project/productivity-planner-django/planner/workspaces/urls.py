from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkspaceListView.as_view(), name='workspace_list'),
    path('new/', views.WorkspaceCreateView.as_view(), name='workspace_create'),
    path('<int:pk>/', views.WorkspaceDetailView.as_view(), name='workspace_detail'),
    path('<int:pk>/edit/', views.WorkspaceUpdateView.as_view(), name='workspace_update'),
    path('<int:pk>/delete/', views.WorkspaceDeleteView.as_view(), name='workspace_delete'),
]
