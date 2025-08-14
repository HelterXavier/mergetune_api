from django.urls import path
from .views import AccountUserView,  AccountUserView, UserPasswordView,  UserPasswordView, LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('/', AccountUserView.as_view(),
         name='create_account'),
    path('/me/', AccountUserView.as_view(), name='user_data'),
    path('/password/', UserPasswordView.as_view(),
         name='update_password'),
    path('/logout/', LogoutView.as_view(), name='logout'),

    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
