import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import MapPhoto
from .gdrive_service import upload_to_drive

# upload photo to google drive
@csrf_exempt
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        folder_name = request.POST.get('folder_name', 'NavMap Photos')

        file_path = f'/tmp/{photo.name}'

        with open(file_path, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)

        google_drive_id = upload_to_drive(file_path, photo.name, folder_name)

        MapPhoto.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            google_drive_id = google_drive_id,
        )

        os.remove(file_path)

        return JsonResponse({
            'id': photo.id,
            'title': photo.title,
            'description': photo.description,
            'google_drive_id': google_drive_id,
            'uploaded_at': photo.uploaded_at,
        })
    else:
        return HttpResponseBadRequest("no photo provided")
    
# get all photos from google drive
def get_photos(request):
    if request.method == 'GET':
        photos = MapPhoto.objects.values('id', 'title', 'description', 'google_drive_id', 'uploaded_at')
        return JsonResponse(list(photos), safe=False)
    else:
        return HttpResponseBadRequest("invalid request method")

def get_photos_by_title(request):
    title = request.GET.get('title')
    if title:
        try:
            photo = MapPhoto.objects.values('id', 'title', 'description', 'google_drive_id', 'uploaded_at').get(title=title)
            return JsonResponse(list(photo), safe=False)
        except MapPhoto.DoesNotExist:
            return HttpResponseBadRequest("photo/s not found")
    else:
        return HttpResponseBadRequest("no title provided")