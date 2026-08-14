from django.urls import path
from .views import CafeAddView, CafeStaffAddView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('cafe/add/', CafeAddView.as_view(), name='cafe-add'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('staff/add/', CafeStaffAddView.as_view(), name='cafe-staff-add'),
]