from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from photai.rename import img_upload, create_thumbnail



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, verbose_name='Category Name', null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_category_url(self):
        return reverse('category', kwargs={'id': self.id})


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(verbose_name='Image Title', max_length=255, null=True)
    photo = models.ImageField(upload_to=img_upload, null=True, max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnail/', null=True, blank=True)
    prompt = models.TextField(null=True)
    price = models.IntegerField(default=0, null=True)
    free = models.BooleanField(default=True, null=True)
    # liked = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    view = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            # Create a thumbnail from the photo
            thumb_file = create_thumbnail(self.photo.path)

            # Save the thumbnail to the thumbnail field
            self.thumbnail.save(thumb_file.name, thumb_file, save=False)
            super().save(*args, **kwargs)

    def get_photo_info_url(self):
        return reverse('details', kwargs={'id': self.id})

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHIOCE = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'))

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, default='Like', choices=LIKE_CHIOCE)

    def __str__(self):
        return str(self.photo)

