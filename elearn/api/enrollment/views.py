from rest_framework import viewsets
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import EnrollSerializer
from .models import Enrollment
from api.student.models import Student
from api.course.models import Course
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def validate_user_session(id,token):
    try:
        user = Student.objects.get(pk=id)
        if user.session_token == token :
            return True
        return False

    except Student.DoesNotExist:
        return False

@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Please re-login', 'code':'1'})

    if request.method == 'POST':
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        corId = request.POST['course']

        try:
            user = Student.objects.get(pk=user_id)
            course = Course.objects.get(pk=corId)
        except Student.DoesNotExist:
            return JsonResponse({'error':'User does not exist'})

        ordr = Enrollment(student=user,course=course,transaction_id=transaction_id,total_amount=amount)
        ordr.save()
        return JsonResponse({'success':True,'error':False,'msg':'Order place Successfully!!'})


class EnrollViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().order_by('id')
    serializer_class = EnrollSerializer
    
