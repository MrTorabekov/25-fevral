from django.urls import path
from apps.views import RegisterApiView,LoginApiView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("login/", LoginApiView.as_view(), name="login"),
]