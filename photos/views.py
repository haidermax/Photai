from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Photo, Like, Category
from photai.rename import get_image_info
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CreatePhotoPostForm
from django.contrib import messages



def category(request, id):
    cat = Category.objects.get(id=id)
    photosList = cat.category.all()

    context = {'listPhotos': photosList}
    return render(request, '', context)

def photoDetails(request, id):
    photo = Photo.objects.get(id=id)
    if photo.deleted:
        messages.success(request, 'Photo not found')
        return redirect('index')
    width, height, format = get_image_info(photo.photo)
    user = request.user

    # Check if the photo has been viewed before
    if 'photo_views' not in request.session:
        request.session['photo_views'] = {}
    photo_views = request.session['photo_views']
    if id not in photo_views:
        photo_views[id] = True
        # Increment the view count of the photo
        photo.view += 1
        photo.save()

    context = {'photo': photo, 'w': width, 'h': height, 'f': format, 'user': user}
    return render(request, 'photos/photo-detail.html', context)

@login_required(login_url='login')
def postCreate(request):
    if request.method == 'POST':
        creationForm = CreatePhotoPostForm(request.POST, request.FILES)
        if creationForm.is_valid():
            new = creationForm.save(commit=False)
            new.uploader = request.user
            new.save()
            return redirect('index')
    else:
        creationForm = CreatePhotoPostForm()
    context = {'form': creationForm}
    return render(request, 'photos/upload.html', context)

@login_required(login_url='login')
def editPost(request, id):
    ePost = Photo.objects.get(id=id)
    if ePost.deleted:
        messages.success(request, 'Photo not found')
        return redirect('index')
    width, height, format = get_image_info(ePost.photo)
    if request.method == 'POST':
        editPhotoForm = CreatePhotoPostForm(request.POST, instance=ePost)
        if editPhotoForm.is_valid():
            editPhotoForm.save()
            messages.success(request, 'Post has been updated successfully.')
            return redirect('details', id=ePost.id)
    editPhotoForm = CreatePhotoPostForm(instance=ePost)
    context = {'editForm': editPhotoForm, 'photo': ePost, 'w': width, 'h': height, 'f': format}
    return render(request, 'photos/editPostPhoto.html', context)


@login_required(login_url=reverse_lazy('login'), redirect_field_name='next')
def like_photo(request):
    user = request.user
    # if user.is_authenticated:
    photo_id = request.POST.get('photo_id')
    if request.method == "POST":
        photo_id = request.POST.get('photo_id')
        photo_obj = Photo.objects.get(id=photo_id)

        if user in photo_obj.liked.all():
            photo_obj.liked.remove(user.id)
        else:
            photo_obj.liked.add(user.id)

        like, created = Like.objects.get_or_create(user=user, photo_id=photo_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

            like.save()
        likes_count = photo_obj.liked.count()
        is_liked = user in photo_obj.liked.all()

        response_data = {
            'likes_count': likes_count,
            'is_liked': is_liked,
        }

        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'not authenticated'})
    # else:
    #     return redirect('login')


def listUploaderPhotos(request, id):
    uploader = User.objects.get(id=id)
    fname = uploader.get_full_name()
    qs = Photo.objects.filter(uploader=id)
    context = {'qs': qs, 'result': fname}
    return render(request, 'index/result.html', context)