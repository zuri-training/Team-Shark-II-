from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.Index.as_view(), name= 'index'),
    path('index/video_detail/<pk>/', views.video_detail, name= 'video_detail'),
    path('password_reset/', views.PasswordReset.as_view(), name ='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name ='password_reset_done'),
    path('confirm_reset/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name ='password_reset_confirm'),
    path('reset_done/', views.PasswordResetComplete.as_view(), name ='password_reset_complete'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('login/', views.LoginView.as_view(next_page='dash'), name= 'login'),
    path('logout/', views.CustomLogout.as_view(next_page='index'), name= 'logout'),
    path('newupload/', views.Upload.as_view(), name= 'upload'),
    path('deleteupload/<int:pk>', views.DeleteUpload.as_view(), name ='deleteupload'),
    path('updateupload/<int:pk>', views.UpdateUpload.as_view(), name ='updateupload'),
    path('myvideos', views.Up.as_view(), name= 'myvideos'),
    path('createpub/', views.PubCreate.as_view(), name= 'createpub'),
    path('delete-pub/<int:pk>', views.DeletePub.as_view(), name ='deletepub'),
    path('update-pub/<int:pk>', views.UpdatePub.as_view(), name ='updatepub'),
    path('schoolnews/', views.Postlist.as_view(), name= 'publist'),
    #path('publications/<slug>/', views.Postdetail.as_view(), name= 'details'),
    path('schoolnews/<slug>/', views.post_detail, name= 'details'),
    path('dashboard', views.Dash.as_view(), name= 'dash'),

]