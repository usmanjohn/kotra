from django.conf import settings

def logo_url(request):
    return {'logo_url': f'{settings.MEDIA_URL}logo/kotrain.png'} 
