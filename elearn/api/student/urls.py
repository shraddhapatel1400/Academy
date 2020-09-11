from rest_framework import routers
from django.urls import path,include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.StudentViewSet)

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/<int:id>/', views.signout, name='signout'),
    path('<int:id>/', views.student_detail),
    path('', include(router.urls))
]