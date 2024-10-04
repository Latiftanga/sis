"""URLS Mapping for the Core API"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('verify-token/', views.verify_token, name="verify-token"),
    path('signup/', views.signup, name='signup'),
    path(
        'add-profile',
        views.add_profile, name='add-profile'
    ),
    path(
        'add-contact',
        views.add_contact, name='add-contact'
    ),
    path('signin/', views.signin, name='signin'),
    path('signout/', LogoutView.as_view(), name='signout' ),
]
