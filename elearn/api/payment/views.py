from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from api.student.models import Student

import braintree

# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="xkp6jj8djpq4z2vw",
        public_key="tw8pdj6p57gbkkms",
        private_key="5885eb920012f1573619c8627e2b2bec"
    )
)


def validate_user_session(id,token):
    try:
        user = Student.objects.get(pk=id)
        if user.session_token == token :
            return True
        return False

    except Student.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request,id,token):

    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,Please login again!!'})
    
    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success':True})


@csrf_exempt
def process_payment(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,Please login again!!'})

    nonce_from_client = request.POST['paymentMethodNonce']
    amount_from_client = request.POST['amount']

    result = gateway.transaction.sale({
        "amount": amount_from_client,
        "payment_method_nonce": nonce_from_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({'success': result.is_success,
                            'transaction': {'id':result.transaction.id, 'amount':result.transaction.amount}
                            })
    else:
        return JsonResponse({'error':True, 'success':False})