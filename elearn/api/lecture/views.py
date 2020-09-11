from django.http import JsonResponse
from rest_framework import viewsets
from .models import Lecture
from .serializers import LectureSerializer

# Create your views here.
class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all().order_by('id')
    serializer_class = LectureSerializer 
   