import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password


def send_activation_email(user, password):
    subject = 'Your Account Activation'
    message = f"Hello {user.email},\n\nYour account has been created. Here is your temporary password: {password}\nPlease log in and change your password immediately."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)
