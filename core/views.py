from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from urllib.request import urlopen
import json
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

#@login_required
def home(request):
    return render(request, 'app.html')

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
        social_user = request.user.social_auth.filter(provider='facebook',).first()
        if social_user:
            url = u'https://graph.facebook.com/{0}/friends?fields=id,name,location,picture&access_token={1}'.format(social_user.uid,social_user.extra_data['access_token'],)
            friends = json.loads(urlopen(url).read()).get('data')
    except:
        facebook_login = None
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})