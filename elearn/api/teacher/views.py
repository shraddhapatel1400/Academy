from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import TeacherSerializer
from .models import Teacher
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password

import datetime
import random
import re

# Create your views here.

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97,123)] + [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error':'Send a Post request with parameter'})

    email = request.POST['email']
    password = request.POST['password']

    if email is not None :
        if not re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", email):
            return JsonResponse({'error':'Enter a valid email'})
    else :
        return JsonResponse({'error': 'Please provide your email'})

    if password is None :
        return JsonResponse({'error': 'Please provide your password'})

    try:
        user = Teacher.objects.get(email=email)

        if check_password(password,user.password) :
            usr_dict = Teacher.objects.filter(email=email).values().first()
            usr_dict.pop('password')

            if user.session_token != '0':
                user.session_token = "0"
                user.save()
                return JsonResponse({'error':'You are already logged in!!'})

            token = generate_session_token()
            user.session_token = token
            user.save()

            login(request,user)
            return JsonResponse({'token':token,'user':usr_dict})
        else :
            return JsonResponse({'error': 'Invalid Password!'})
        
    except Teacher.DoesNotExist:
        return JsonResponse({'error':'Invalid email'})


def signout(request,id):
    logout(request)

    try:
        user = Teacher.objects.get(pk=id)
        user.session_token = "0"
        user.last_login = datetime.datetime.now()
        user.save()

    except Teacher.DoesNotExist:
        return JsonResponse({'error':'Invalid user ID'})

    return JsonResponse({'success':'Logged out Successfully!!'})

@api_view(['GET', 'PATCH', 'DELETE'])
def teacher_detail(request,id):
    try: 
        teacher = Teacher.objects.get(pk=id)

        if request.method == 'GET': 
            teacher_serializer = TeacherSerializer(teacher) 
            return JsonResponse(teacher_serializer.data) 

        elif request.method == 'PATCH': 
            teacher_data = JSONParser().parse(request) 
            teacher_serializer = TeacherSerializer(teacher, data=teacher_data, partial=True) 
            if teacher_serializer.is_valid(): 
                teacher_serializer.save() 
                return JsonResponse(teacher_serializer.data) 
            return JsonResponse(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        elif request.method == 'DELETE': 
            teacher.delete() 
            return JsonResponse({'message': 'Teacher was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Teacher.DoesNotExist: 
        return JsonResponse({'message': 'Teacher not exists'}, status=status.HTTP_404_NOT_FOUND) 


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = Teacher.objects.all().order_by('id')
    serializer_class = TeacherSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]