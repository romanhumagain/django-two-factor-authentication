from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm
from .utils import send_otp_to_user, generate_slugs
from datetime import datetime
import pyotp
from django.contrib.auth.models import User
from App.models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Registered Your Account.")
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            send_otp_to_user(request, user)
            messages.success(request, "Successfully Sent OTP.")
            slug = user.profile.slug
            return redirect(f'/otp/{slug}/')
        else:
            messages.error(request, "Invalid Credentials")
    else:
        form = UserLoginForm()

    return render(request, 'app/login.html', {'form': form})
  
def otp_verification(request, slug):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        
        if otp_valid_date:
            valid_until = datetime.fromisoformat(otp_valid_date)  
                
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            
            if valid_until > datetime.now():
            
              totp = pyotp.TOTP(otp_secret_key, interval=60)
              if totp.verify(otp):
                  username = request.session.get('username')
                  user = get_object_or_404(User, username=username)
                  login(request, user)

                  # Cleanup session
                  del request.session['username']
                  del request.session['otp_secret_key']
                  del request.session['otp_valid_date']

                  return redirect('profile')
              else:
                  messages.error(request, "Invalid OTP")
            else:
                  messages.error(request, "Sorry Session Expired !!")
        else:
              messages.error(request, "Something went wrong !")
    return render(request, 'app/otp.html', {'slug':slug})
  

def otp_verification_resend(request, slug):
  profile = Profile.objects.get(slug = slug)
  user = profile.user
  otp_secret_key = request.session.get('otp_secret_key')
  otp_valid_date = request.session.get('otp_valid_date')
  
  del request.session['otp_secret_key']
  del request.session['otp_valid_date']
  
  send_otp_to_user(request, user)
  messages.success(request, 'Successfully Resent OTP.')
  return redirect(f'/otp/{slug}/')

@login_required
def profile_view(request):
    return render(request, 'app/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
