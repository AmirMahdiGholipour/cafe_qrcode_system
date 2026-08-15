# accounts/urls.py
from django.urls import path
from .views import SignupView, CafeAddView, StaffAddView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("cafe/add/", CafeAddView.as_view(), name="cafe-add"),
    path("cafes/<int:cafe_id>/staff/add/", StaffAddView.as_view(), name="staff-add"),
]