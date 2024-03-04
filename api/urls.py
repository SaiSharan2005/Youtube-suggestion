from django.urls import path
from . import views

urlpatterns = [
    path("dam",views.home,name= "home"),
]