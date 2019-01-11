## This file processes the remaining URL after the
## host portion of the original URL has been stripped.

## URL mapping calls on Django's URL function.

from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
