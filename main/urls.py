from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name= "home"),
    path("home",views.nonLogInUser,name="non-login-home"),
    path("learner",views.learner,name  ="learner"),
    path("courses/",views.courses, name = "courses"),
    path("lecture/<str:Topic>/<str:SubTopic>/",views.lecture,name = "lecture"),
    path("topic/<str:Topic>", views.topic,name = "topic"),
    path('sign_up/',views.sign_up,name = "signup"),
    path('log_in/',views.log_in,name = "login"),
    path('log_out/',views.log_out,name = "logout"),
]