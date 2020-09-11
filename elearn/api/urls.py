from django.urls import path,include
from rest_framework.authtoken import views

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('student/', include('api.student.urls')),
    path('teacher/', include('api.teacher.urls')),
    path('course/', include('api.course.urls')),
    path('adminp/', include('api.adminpanel.urls')),
    path('enroll/', include('api.enrollment.urls')),
    path('payment/', include('api.payment.urls')),
    path('lecture/', include('api.lecture.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]