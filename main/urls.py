from django.urls import path
from . import views, api
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.nonLogInUser, name="non-login-home"),
    path("learner", views.learner, name="learner"),
    path("courses/", views.courses, name="courses"),
    path("lecture/<str:Topic>/<str:SubTopic>/", views.lecture, name="lecture"),
    path("topic/<str:Topic>", views.topic, name="topic"),
    path('sign_up/', views.sign_up, name="signup"),
    path('log_in/', views.log_in, name="login"),
    path('log_out/', views.log_out, name="logout"),

    path('AllCategory/', api.AllCategoryView.as_view()),
    path('Category/<int:pk>', api.CategoryView.as_view()),
    path('SubCourse/', api.SubCourse.as_view()),
    path('SubCourse/<int:pk>', api.SubCourse.as_view()),
    path('SubTopic/', api.SubTopic.as_view()),
    path('SubTopic/<int:pk>', api.SubTopic.as_view()),
    path("WholeCourse/<int:pk>", api.WholeCourse),
    path("GetUserData/", api.GetUserData.as_view(), name="GetUserData"),
    path("Document/<int:pk>",api.DocumentationView.as_view(), name="Document"),
    path("DocumentData/<int:pk>",api.DocumentationDataView.as_view(), name="DocumentData"),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/login", api.LoginView.as_view(), name="login"),
    path("api/logout_user/", api.LogoutUserView.as_view(), name="logout_user"),
    path("api/register", api.UserRegisterView.as_view(), name="register"),

]
