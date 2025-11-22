from django.shortcuts import render
from django.contrib.auth.hashers import make_password ,check_password
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core import serializers
import json
# Create your views here.
        # user = authenticate(username=email,password=password)


def serFix(data, fields=True):
    if fields == True:
        return json.loads(serializers.serialize('json',data))[0]['fields']
    return json.loads(serializers.serialize('json',data))


@csrf_exempt
@api_view(['POST'])
def createAccount(request):
    if request.method == 'POST':
        userName = request.data.get('userName')
        email = request.data.get('email')
        password = request.data.get('password')
        password=make_password(password)
          #if username and email and password 
        if userName == None:
            return JsonResponse({
                'message': 'userName is not founded',
                'status':500,
            },status=500)
        
        if email == None:
            return JsonResponse({
                'message': 'email is not founded',
                'status':500,
            },status=500)
        
        if password == None:
            return JsonResponse({
                'message': 'password is not founded',
                'status':500,
            },status=500)
        
        
        emailWithFilter = User.objects.filter(email=email)

        if emailWithFilter:
            return JsonResponse({
                'message': 'email is already exists',
                'status':500,
            },status=500)
        
    


       #email
        try:
            User.objects.create(userName=userName, email=email,password=password).save()
            
            emailWithFilter = User.objects.filter(email=email)

            return JsonResponse({
                'user': {
                    'userName': serFix(emailWithFilter)['userName'],
                    'email': serFix(emailWithFilter)['email']
                },
                'message': 'account has been created',
                'status':200,
            },status=200)
        except:
            return JsonResponse({
                'message': 'An error occurred during login',
                'status':500,
            },status=500)
        #hashing passsword
    try:
            User.objects.create(userName=userName, email=email, password=password)
            emailWithFilter = User.objects.filter(email=email)
            return JsonResponse({
                'user': {
                    'userName': serFix(emailWithFilter)['userName'],
                    'email': serFix(emailWithFilter)['email']
                },
                'message': 'account has been created',
                'status':200,
            },status=200)
    except:
            return JsonResponse({
                'message': 'An error occurred during login',
                'status':500,
            },status=500)

@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # التحقق من صحة الإدخالات
        if email == None:
            return JsonResponse({
                'message': 'email is not founded',
                'status':500,
            },status=500)
        if password == None:
            return JsonResponse({
                'message': 'password is not founded',
                'status':500,
            },status=500)

        # التحقق من وجود المستخدم وصحة كلمة المرور
        user = User.objects.filter(email=email)
        if user:
            userPassword = serFix(user)['password']
            password_match = check_password(password, userPassword)
            if password_match:
                return JsonResponse({
                    'user': {
                        'userName':serFix(user)['userName'],
                        'email':serFix(user)['email']
                    },
                    'message': 'login is successfully',
                    'status':200,
                },status=200)
        return JsonResponse({
            'message': "please check ur email ir password and try again later . . .",
            'status':500,
        },status=500)

