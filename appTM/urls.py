from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# url patterns for page navigation
urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('uncomplete/<int:pk>/', views.uncomplete_task, name='uncomplete_task'),
    path('completed/', views.tasks_complete, name='tasks_complete'),
    path('task/<int:pk>/flag/', views.task_flag, name='task_flag'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
