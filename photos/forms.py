from django import forms
from .models import Photo




class CreatePhotoPostForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['category', 'title', 'photo', 'prompt', 'deleted']