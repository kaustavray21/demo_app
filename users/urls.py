from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('user_login_history/<int:user_id>/', views.user_login_history_view, name='user_login_history'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
]
