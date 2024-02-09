from django.shortcuts import render
from photos.models import Photo, Like
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





def search(request):
    searched =request.GET.get('search')
    qs = Photo.objects.filter(Q(title__icontains=searched,deleted=False)|Q(prompt__icontains=searched,deleted=False)).distinct()
    context = {'result': searched, 'qs': qs}
    return render(request, 'index/result.html', context)


def index(request):
    # Get all non-deleted Photo objects and order them by creation date
    photos_list = Photo.objects.filter(deleted=False).order_by('-created')

    # Configure pagination
    page = request.GET.get('page')
    paginator = Paginator(photos_list, 12)  # Show 12 photos per page (or any number you prefer)

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results
        photos = paginator.page(paginator.num_pages)


    context = {'photos': photos}
    return render(request, 'index/index.html', context)



# def index(request):
#     return render(request, 'index/index.html')
