
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from common.services.mail import MyMail

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

def send_account_activation_email(
    verification_link,
    user_first_name,
    user_email,
) : 
    subject = 'Verify your account'
    body = render_to_string('user_verification_email.html',{
        'user_name': user_first_name,
        'verification_link': verification_link,
    })
    email_address = user_email
    print(verification_link)
    activation_mail = MyMail(subject, body, email_address)
    activation_mail.send()