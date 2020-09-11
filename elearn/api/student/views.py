from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import StudentSerializer
from .models import Student
from django.http import JsonResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password, make_password

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
        user = Student.objects.get(email=email)

        if check_password(password,user.password) :
            usr_dict = Student.objects.filter(email=email).values().first()
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

    except Student.DoesNotExist:
        return JsonResponse({'error':'Invalid email'})


def signout(request,id):
    logout(request)

    try:
        user = Student.objects.get(pk=id)
        user.session_token = "0"
        user.last_login = datetime.datetime.now()
        user.save()

    except Student.DoesNotExist:
        return JsonResponse({'error':'Invalid user ID'})

    return JsonResponse({'success':'Logged out Successfully!!'})


@api_view(['GET','PATCH', 'DELETE'])
def student_detail(request,id):
    try: 
        student = Student.objects.get(pk=id)

        if request.method == 'GET': 
            student_serializer = StudentSerializer(student) 
            return JsonResponse(student_serializer.data) 

        elif request.method == 'PATCH': 
            student_data = JSONParser().parse(request) 
            student_serializer = StudentSerializer(student, data=student_data, partial=True) 
            if student_serializer.is_valid(): 
                student_serializer.save() 
                return JsonResponse(student_serializer.data) 
            return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        elif request.method == 'DELETE': 
            student.delete() 
            return JsonResponse({'message': 'Student was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Student.DoesNotExist: 
        return JsonResponse({'message': 'Student not exists'}, status=status.HTTP_404_NOT_FOUND) 



class StudentViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]