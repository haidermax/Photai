from django.core.exceptions import ValidationError



def validate_phone(value):
    if value.startswith(('077','078','075')) and len(value) == 11:
        return value
    else:
        raise ValidationError('Not a Phone Format')



def validate_photo(value):
    if value.endwith(('.jpeg', '.jpg', '.png')):
        return value
    else:
        raise ValidationError('Not a Photo Format')