from rest_framework import routers
from django.urls import path,include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signout/<int:id>/', views.signout, name='signout'),
    path('<int:id>/', views.admin_detail),
    path('', include(router.urls))
]