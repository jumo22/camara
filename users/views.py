from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from announcements.decorators import allowed_users
from .models import Profile
from .tokens import account_activation_token


@login_required
@allowed_users(allowed_roles=['Boardie'])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}! Activation email was sent!')
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # context = {'uidb64': uidb64 }
        return redirect('password_reset')
    else:
        return HttpResponse('Activation link is invalid!')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/members.html'
    context_object_name = 'profiles'
    ordering = ['user__last_name']
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(user__username="admin")

# @login_required
# def profile_detail(request, uid):
#     user = User.objects.get(pk=uid)
#     return render(request, 'users/profile_detail.html', {'user': user})

#     def get_user_profile(request, username):
#         user = User.objects.get(username=username)
#         return render(request, '<app_name>/user_profile.html', {"user": user})
#
#
# def view_profile(request, pk=None):
#     if pk:
#         user = User.objects.get(pk=pk)
#     else:
#         user = request.user
#     args = {'user': user}
#     return render(request, 'accounts/profile.html', args)

