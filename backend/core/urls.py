from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.Index.as_view(), name= 'index'),
    path('password_reset/', views.PasswordReset.as_view(), name ='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name ='password_reset_done'),
    path('confirm_reset/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name ='password_reset_confirm'),
    path('reset_done/', views.PasswordResetComplete.as_view(), name ='password_reset_complete'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(next_page='index'), name= 'login'),
    path('logout/', views.CustomLogout.as_view(next_page='index'), name= 'logout'),

]