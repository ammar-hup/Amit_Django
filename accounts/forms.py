from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    

class ActivisionSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    activision_id = forms.CharField(max_length=50, required=False, label="Activision ID (optional)")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'activision_id', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

