from django.urls import path
from rest_framework import routers

from education.apps import EducationConfig
from education.views import *

app_name = EducationConfig.name

router = routers.SimpleRouter()
router.register('course', CourseViewSet)
router.register('payment', PaymentViewSet)

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
] + router.urls
