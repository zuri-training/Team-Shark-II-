from django.forms import  ModelForm
from .models import CustomUser, Comment


class RegisterForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = ['full_name', 'username', 'email', 'password']


class ForgotPwdForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = [ 'email', ]


class LoginForm(ModelForm):
    class Meta:
        model =CustomUser
        fields = ['username', 'password']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('user', 'real')


