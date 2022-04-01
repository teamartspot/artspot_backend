
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from common.services.mail import MyMail
from rest_framework_simplejwt.tokens import RefreshToken

#Create User
def create_user(
    *,
    first_name,
    last_name,
    email,
    password,
    password2
) -> User:
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_customer=True,
        is_seller=False,
        password=password,
    )

    user.full_clean()
    user.save()
    return user

def send_email(subject, body, email_address):
    try:
        activation_mail = MyMail(subject, body, email_address)
        activation_mail.send()
    except Exception as e:
        raise e

# Send account activation email
def send_account_activation_email(user, current_site) : 

    email_address = user.email
    user_first_name = user.first_name
    token = RefreshToken.for_user(user).access_token
    current_site = current_site
    relative_link = '/users/verify/'
    verification_link = 'https://' + str(current_site) + relative_link + "?token=" + str(token)
    subject = 'Verify your account'
    body = render_to_string('user_verification_email.html',{
        'user_name': user_first_name,
        'verification_link': verification_link,
    })
    print(verification_link)
    send_email(subject, body, email_address)

# Send reset password email
def send_reset_password_email(user, current_site):

    email_address = user.email
    user_first_name = user.first_name
    current_site = current_site
    token = RefreshToken.for_user(user).access_token
    relative_link = 'reset_password/confirm/'
    reset_password_link = 'https://' + str(current_site) + relative_link + "?token=" + str(token)
    subject = 'Reset your password'
    body = render_to_string('user_reset_password_email.html',{
        'user_name': user_first_name,
        'reset_password_link': reset_password_link,
    })
   
    print(reset_password_link)
    send_email(subject, body, email_address)