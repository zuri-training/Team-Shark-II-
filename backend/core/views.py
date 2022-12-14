from django.views.generic import ListView
from .models import Reel, Category
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse_lazy
from .forms import *
from .models import CustomUser
from django.http import HttpRequest, HttpResponse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, FormView, PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,  force_str
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.token import account_activation_token
from django.core.paginator import Paginator
from django.core.mail import send_mail



class PasswordReset(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name ='password_reset_email.html'
    subject_template_name ='password_reset_subject.txt'
    extra_email_context = None

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
    
    
class PasswordResetComplete(PasswordResetDoneView):
    template_name = 'password_reset_complete.html'


class Index(ListView):
    model = Reel
    template_name ='index.html'
    context_object_name = 'reels'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()

        return context


class Register(FormView):
    form_class = RegisterForm
    template_name = 'sign.html'
    redirect_authenticated_user = True
    
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            user =form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active =False
            user.save()
            
            current_site = get_current_site(request)
            subject ='Activate Your Account'
            message =render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please ' + user.username + ' Confirm your email to complete registration'))
            return redirect('register')
        return render(request, self.template_name, {'form':form})


    
    
    
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user =CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user =None
            
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active =True
            user.save()
            messages.success(request, ('Your account has been confirmed. Please Login Now'))
            return redirect('login')
        else:
            messages.warning(request, ('Validation of account fatally failed'))
            return redirect('login')
            


class LoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True


class CustomLogout(LogoutView):
    pass