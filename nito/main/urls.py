from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login, name="login"),
    url(r'^randompost/', views.randompost, name="randompost"),
    url(r'^submitpost/', views.submitpost, name="submitpost"),
    url(r'^', views.index,name="index")
]
