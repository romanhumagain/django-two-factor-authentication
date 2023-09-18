import pyotp
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.text import slugify
import uuid

def generate_slugs(modal_class, title: str) -> str:
    slug = slugify(f"{title}-{uuid.uuid4()}")
    while modal_class.objects.filter(slug=slug).exists():
        slug = slugify(f"{title}-{uuid.uuid4()}")
    return slug



def send_email(subject, message, to):
  mail = EmailMultiAlternatives(
    subject=subject,
    body = message,
    to =[to],
    from_email=settings.EMAIL_HOST_USER
  )
  mail.content_subtype = 'html'
  mail.send()



def send_otp_to_user(request, user):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    
    valid_date = datetime.now() + timedelta(minutes=1)
    
    request.session['otp_valid_date'] = valid_date.isoformat() #converting the datetime to string
    
    request.session['username'] = user.username
    
    # You can replace the print statement with actual logic to send the OTP to the user.
    print(f"Your one-time password is {otp}")
    subject = "OTP Code !!"
    
    message = ( 
           f"<p> Dear {user.username},</p>"

           f"<p> Thank you for using ..... Platform. As part of our commitment to protect your account, we've generated a one-time password for your recent login attempt.</p>"
           f'<p> Your OTP Code: <a href =""><strong>{otp}</strong></a></p>'
             
    )
    send_email(subject, message,user.email )
