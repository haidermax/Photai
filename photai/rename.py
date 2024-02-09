import os
import uuid
from PIL import Image


# Generate a random UUID
uuid_4 = uuid.uuid4()

# Convert the UUID to a string
uuid_string = str(uuid_4)

# Split the string into a list of substrings based on the '-' character
uuid_list = uuid_string.split('-')

nameImg = uuid_list[-1]

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def get_image_info(filepath):
    with Image.open(filepath) as img:
        width, height = img.size
        format = img.format
    return width, height, format

def img_upload(instance, filename):
    # new_name = instance.title
    name, ext = get_filename_ext(filename)
    final_name = f'{nameImg}{ext}'
    return f'uploaded_photos/{final_name}'


from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def create_thumbnail(image_path):
    with Image.open(image_path) as img:
        # Resize the image to 200x200
        # img.thumbnail((200, 200))

        # Compress the image and save it to a BytesIO object
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=30)

        # Create a new InMemoryUploadedFile object for the thumbnail image
        thumb_file = InMemoryUploadedFile(thumb_io, None, f'{nameImg}_thumb.jpg', 'image/jpeg', thumb_io.getbuffer().nbytes, None)

        return thumb_file



# def create_thumbnail(instance, filename):
#     # Define the thumbnail size
#     thumb_size = (300, 300)
#
#     # Open the original image using Pillow
#     with Image.open(instance.photo.path) as img:
#         # Create the thumbnail using Pillow
#         img.thumbnail(thumb_size)
#
#         # Get the filename and extension of the original file
#         name, ext = os.path.splitext(filename)
#
#         # Create a new filename for the thumbnail
#         thumb_name = f"{name}_thumb{ext}"
#
#         # Save the thumbnail to the media directory
#         thumb_path = os.path.join("thumbnails", thumb_name)
#         thumb_full_path = os.path.join(settings.MEDIA_ROOT, thumb_path)
#         img.save(thumb_full_path)
#
#     # Return the thumbnail path to be saved to the Photo model
#     return thumb_path
