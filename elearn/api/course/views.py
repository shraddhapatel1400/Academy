from rest_framework import viewsets
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import CourseSerializer
from .models import Course
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
# Create your views here.

@api_view(['GET', 'PATCH', 'DELETE'])
def course_detail(request,id):
    try: 
        course = Course.objects.get(pk=id)

        if request.method == 'GET': 
            course_serializer = CourseSerializer(course) 
            return JsonResponse(course_serializer.data) 

        elif request.method == 'PATCH': 
            course_data = JSONParser().parse(request) 
            course_serializer = CourseSerializer(course, data=course_data, partial=True) 
            if course_serializer.is_valid(): 
                course_serializer.save() 
                return JsonResponse(course_serializer.data) 
            return JsonResponse(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        elif request.method == 'DELETE': 
            course.delete() 
            return JsonResponse({'message': 'Course was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Course.DoesNotExist: 
        return JsonResponse({'message': 'Course not exists'}, status=status.HTTP_404_NOT_FOUND) 


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer 
   