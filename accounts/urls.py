from django.urls import path
from django.shortcuts import render

from . import views

urlpatterns = [
    # path('signup/', signup, name='signup'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activation-sent/', lambda r: render(r, 'accounts/activation_sent.html'), name='activation_sent'),
]
