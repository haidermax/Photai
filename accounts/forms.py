from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ImageField, FileInput



class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            user = super(RegisterationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user


class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password']


class EditCustomProfile(forms.ModelForm):

    profileImg = ImageField(widget=FileInput)
    class Meta:
        model = UserProfile
        
        fields = ['profileImg', 'phone', 'facebook', 'twitter', 'instagram']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)