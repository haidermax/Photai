from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash,authenticate
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View
from .tokens import account_activation_token,account_reset_token
from django.contrib.auth.decorators import login_required
from .forms import *
from photos.models import Photo
from photai.emailFunction import send_email
from photai.decorators import redirect_authenticated_user
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = LoginForm()
        message = ''
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    message = f'Hello {user.username}! You have been logged in'
                    return redirect('index')
                else:
                    message = 'Login failed!'
        return render(
            request, 'accounts/login.html', context={'form': form, 'message': message})


@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        cform = CaptchaForm(request.POST)
        if form.is_valid() and cform.is_valid():
            user = form.save(commit=False)
            human = True
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # Call the send_email function instead of using EmailMessage
            send_email(to_email, subject, message)
            messages.success(request, f'Thank you a activation link send to your email, check your email {to_email}')
            return redirect('index')
    else:
        form = RegisterationForm()
        cform = CaptchaForm()
    context = {'form': form, 'cform': cform}
    return render(request, 'accounts/register.html', context)
def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        login(request, user)
        messages.success(request, 'Thank you for your confirmation')     
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid!')
# def password_reset_request(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             current_site = get_current_site(request)
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "accounts/password_reset_email.txt"
#                     c = {
#                     "email":user.email,
#                     'domain':current_site.domain,
#                     'site_name': 'PhotAI',
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "user": user,
#                     'token': account_activation_token.make_token(user),
#                     'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     send_email(data, subject, email)
#                     return redirect("password_reset_done")
#     password_reset_form = PasswordResetForm()

#     context = {"form": password_reset_form}
#     return render(request, "accounts/password_reset.html", context)




# @login_required(login_url='login')
# def user_type_redirect(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         return redirect('login')


@login_required(login_url='login')
def user_profile(request):
    # ownedPhotos = Photo.objects.filter(Q(uploader=request.user.id) | Q(deleted=False)).order_by('-created')
    ownedPhotos = Photo.objects.filter(uploader=request.user.id).order_by('-created')
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        sub_form = EditCustomProfile(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and sub_form.is_valid():
            form.save()
            sub_form.save()
            messages.success(request, 'Changes has been added')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        sub_form = EditCustomProfile(instance=request.user.userprofile)


    context = {'form': form, 'sub_form': sub_form}
    return render(request, 'accounts/profile.html', context)
class PasswordResetView(View):
    def get(self, request):
        return render(request, 'accounts/password_reset.html')
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email address')
            return redirect('password_reset')
        # Generate a UUID token for the user
        token = str(uuid.uuid4())
        current_site = get_current_site(request)
        # Send an email to the user with the password reset link
        message = render_to_string('accounts/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_reset_token.make_token(user),
        })
        message
        mail_subject = 'Reset your password'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Please check your email to reset your password')
        return redirect('login')
class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            print(uid)
            user = User.objects.get(pk=uid)
            print(user.first_name)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_reset_token.check_token(user, token):
            request.session['reset_password_user_id'] = user.id
            return render(request, 'accounts/password_reset_confirm.html')

        messages.error(request, 'Invalid reset link')
        return redirect('password_reset')

    def post(self, request, uidb64, token):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('password_reset_confirm', uidb64=uidb64, token=token)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            print(user.first_name)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_reset_token.check_token(user, token):
            # Set the user's new password
            user.set_password(password1)
            user.save()
            print(user.password)
            print("ok")
            messages.success(request, 'Your password has been reset. Please log in')
            return redirect('password_reset_complete')

        messages.error(request, 'Invalid reset link')
        print(messages.error)
        return redirect('password_reset_confirm', uidb64=uidb64, token=token)
