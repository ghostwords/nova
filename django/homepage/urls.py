from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^privacy$', views.privacy, name='privacy'),
    url(r'^privacy.html$', views.privacy, name='privacy'),
    url(r'^survey$', views.survey, name='survey'),
]
