from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .forms import ActivisionSignupForm
from .models import CustomUser
from .utils import account_activation_token
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    context = {
        'form': form,
        'title': 'Sign Up',
    }
    return render(request, 'registration/signup.html', context)

# ---------- SIGNUP + EMAIL CONFIRM ----------
class SignupView(View):
    def get(self, request):
        form = ActivisionSignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = ActivisionSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your AMIT Blog account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                mail_subject,
                message,
                'Amit_Test_Blog@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('activation_sent')
        return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/activation_complete.html')
    else:
        return render(request, 'registration/activation_invalid.html')

