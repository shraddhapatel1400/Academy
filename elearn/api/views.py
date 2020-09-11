from django.http import JsonResponse

# Create your views here.

def home(request):
    return JsonResponse({'Name':'Shraddha','Course':'Django-React'})