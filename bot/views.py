from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.hashers import make_password ,check_password, get_hasher
from .models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core import serializers
import json
# Create your views here.


def serFix(data, fields=True):
    if fields == True:
        return json.loads(serializers.serialize('json',data))[0]['fields']
    return json.loads(serializers.serialize('json',data))

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

@csrf_exempt
@api_view(['POST'])
def createAccount(request):
    if request.method == 'POST':
        userName = request.data.get('userName')
        email = request.data.get('email')
        password = request.data.get('password')

        # التحقق من صحة الإدخالات
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

        # التحقق من عدم وجود البريد الإلكتروني مسبقًا
        emailWithFilter = User.objects.filter(email=email)
        if emailWithFilter:
            return JsonResponse({
                'message': 'email is already exists',
                'status':500,
            },status=500)

        # إنشاء الحساب وتخزين كلمة المرور المشفرة
        hashed_password = make_password(password)
        try:
            User.objects.create(userName=userName, email=email, password=hashed_password)
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