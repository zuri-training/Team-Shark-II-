from django.views.generic import ListView
from .models import Reel, Category, PostComments, Posts
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
from django.contrib.auth.decorators import login_required


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
        context['latestnews'] = Posts.objects.all()


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
            user.is_active = True
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


class Dash(ListView):
    model = Reel
    template_name ='dashboard.html'
    context_object_name = 'reels'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['latestnews'] = Posts.objects.all()


        return context


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



@login_required(login_url='login')
def video_detail(request, pk):
    #similar posts starts here
    pub = Reel.objects.get(pk=pk)
    related = Reel.objects.filter(category=pub.category)

    #comment starts here
    post = get_object_or_404(Reel, pk=pk)
    comments = pub.commented.filter(active=True).order_by('-date')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.user =request.user
            comment_form.instance.real = post
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()

    context = {
        'pub': pub,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'related': related,
    }
    return render(request, 'vid.html', context)



class Up(LoginRequiredMixin, ListView):
    model = Reel
    template_name ='up.html'
    context_object_name = 'reels'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['myvid'] = Reel.objects.filter(uploader=self.request.user)

        return context


class Upload(LoginRequiredMixin,  CreateView):
    model = Reel
    template_name = 'upload.html'
    fields = ['title','category', 'description', 'cover_thumbnail', 'video']

    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super(Upload, self).form_valid(form)


class UpdateUpload(LoginRequiredMixin,  UpdateView):
    model = Reel
    fields = ['title', 'description', 'video']
    template_name = 'upload.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('video_detail', kwargs={'pk': self.object.pk})


class Postlist(ListView):
    model = Posts
    template_name = 'pubs.html'
    context_object_name = 'posts'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['logos'] = Logo.objects.all()
        context['publications'] = Posts.objects.all()
        return context


class DeleteUpload(LoginRequiredMixin,  DeleteView):
    model = Reel
    template_name = 'deleteupload.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class PubCreate(LoginRequiredMixin,  CreateView):
    model = Posts
    template_name = 'createpub.html'
    fields = ['title', 'description', 'image']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PubCreate, self).form_valid(form)


class UpdatePub(LoginRequiredMixin,  UpdateView):
    model = Posts
    fields = ['title', 'description', 'image']
    template_name = 'createpub.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.object.slug})


class DeletePub(LoginRequiredMixin,  DeleteView):
    model = Posts
    template_name = 'deletepub.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('publications')


def post_detail(request, slug):
    # similar posts starts here
    pub = Posts.objects.get(slug=slug)
    # comment starts here
    post = get_object_or_404(Posts, slug=slug)
    comments = pub.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'pub': pub,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'details.html', context)
