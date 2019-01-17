## This file processes the remaining URL after the
## host portion of the original URL has been stripped.

## URL mapping calls on Django's URL function.

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name = 'about'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
