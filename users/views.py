# users/views.py

from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import UserRegisterForm, UserProfileUpdateForm, UserUpdateForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView, DeleteView,DetailView,UpdateView, CreateView
from django.core.paginator import Paginator
from topics.models import Upvoter, UpvoterAnswer, Topic, Answer
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from users import tokens
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import account_activation_token
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, Sum, F, IntegerField, Case, When, Value
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm, UserProfileUpdateForm, EmailChangeForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth import views as auth_views
User = get_user_model()



from django.db import transaction

@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # This will trigger the signals to create and save the UserProfile
            
            user_image = form.cleaned_data.get('user_image')
            if user_image:
                user.userprofile.image = user_image
                user.userprofile.save()

            # Email verification logic
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.warning(request, 'You are not logged in yet. Please verify your account through message we sent through your email address')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.userprofile.is_email_verified = True
        user.userprofile.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Your account is now fully activated.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                
                login(request, user)
                next_url = request.GET.get('next', '/')  # Default redirect to home if 'next' isn't provided
                return redirect(next_url)
                    
            else:
                form.add_error(None, 'Invalid username or Password')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})

@login_required
def LogOut(request):
    auth_logout(request)
    return redirect('/')

def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    topics = Topic.objects.filter(topic_author = profile_user)
    
    
    books = profile_user.books_uploaded.all()

    saved_topics = profile_user.saved_topics.all()
    tutorials = profile_user.tutoring.all()
    is_own_profile = request.user.is_authenticated and request.user == profile_user
    
    context = {
        'profile_user': profile_user,
        'topics':topics,
        'is_own_profile': is_own_profile,
        'saved_topics':saved_topics,
        'books':books,
        'tutorials':tutorials
    }
    return render(request, 'users/view_profile.html', context)


@login_required
def update_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user != profile_user:
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=profile_user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile_user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile', username=profile_user.username)
    else:
        u_form = UserUpdateForm(instance=profile_user)
        p_form = UserProfileUpdateForm(instance=profile_user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile_user': profile_user
    }
    return render(request, 'users/update_profile.html', context)




@login_required
def update_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            request.user.userprofile.new_email = new_email
            request.user.userprofile.save()

            # Send verification email
            current_site = get_current_site(request)
            subject = 'Verify your new email address'
            message = render_to_string('users/email_change_verification.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token': account_activation_token.make_token(request.user),
                'new_email': new_email
            })
            send_mail(subject, message, 'noreply@yourdomain.com', [new_email])
            messages.success(request, 'Please check your new email to confirm the change.')
            return redirect('profile', username=request.user.username)
    else:
        form = EmailChangeForm(request.user)
    return render(request, 'users/update_email.html', {'form': form})
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.email = user.userprofile.new_email
        user.userprofile.new_email = ''
        user.save()
        user.userprofile.save()
        messages.success(request, 'Your email has been successfully updated.')
    else:
        messages.error(request, 'The verification link was invalid or has expired.')
    
    return redirect('profile', username=request.user.username)

class UsersList(ListView):
    model = User
    paginate_by = 9
    ordering = ['username']
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')

        queryset = User.objects.all().select_related('userprofile').order_by('username')

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(userprofile__bio__icontains=query)
            ).order_by('username')

        

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context