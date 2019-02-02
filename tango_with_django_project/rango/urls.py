## This file processes the remaining URL after the
## host portion of the original URL has been stripped.

## URL mapping calls on Django's URL function.

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rango import views

app_name = 'rango'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^about$', views.about, name = 'about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name = 'show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',\
     views.add_page, name='add_page')
]
