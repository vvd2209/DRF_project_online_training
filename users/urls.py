from django.urls import path

from users.apps import UsersConfig

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment/', views.PaymentListView.as_view(), name='payments'),
]
