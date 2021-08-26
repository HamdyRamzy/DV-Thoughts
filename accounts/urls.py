from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.contrib.auth import views as  auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True ,template_name='login.html'), name='login'),
    path('settings/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('settings/change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

]
