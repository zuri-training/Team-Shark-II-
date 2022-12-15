from django.contrib import admin
from django.urls import path
from greenhood_app.views import HomeView, LoginView, RegisterView, LogoutView, NewVideo, VideoView, VideoFileView, CommentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view()),
    path('signup/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('new_video', NewVideo.as_view()),
    path('comment', CommentView.as_view()),
    path('get_video/<file_name>', VideoFileView.as_view()),
    path('video/<int:id>', VideoView.as_view()),  
]
