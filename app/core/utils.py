import random
import string
import secrets
from django.core.mail import send_mail
from django.conf import settings

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password


def send_activation_email(email, password):
    subject = 'Your Account Activation'
    message = f"Hello {email},\n\nYour account has been created. Here is your temporary password: {password}\nPlease log in and change your password immediately."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)


def generate_unique_token(length=10):
    # Define the characters to use for the token
    characters = string.ascii_letters + string.digits
    # Generate a secure random token
    token = ''.join(secrets.choice(characters) for _ in range(length)).upper()
    return token
