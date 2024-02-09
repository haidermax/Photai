from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from photai.utils import validate_phone

def user_directory_path(instance, filename):
    emailName = instance.user.email.split('@')[0]
    return f'profile_img/%Y/%m/{emailName}/{filename}'

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImg = models.ImageField('User Picture', upload_to=user_directory_path, default='profile_img/avatar.png')
    phone = models.CharField(max_length=11, blank=True, null=True, validators=[validate_phone], help_text='077 or 078 or 075')
    facebook = models.URLField(default=None, null=True, blank=True)
    twitter = models.URLField(default=None, null=True, blank=True)
    instagram = models.URLField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.get_full_name()



# Save created UserProfile with User
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
