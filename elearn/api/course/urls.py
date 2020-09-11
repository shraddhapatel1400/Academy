from rest_framework import routers
from django.urls import path,include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/', views.course_detail)
]