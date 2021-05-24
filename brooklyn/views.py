# from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from django.contrib.auth import login
# from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from django.shortcuts import render
# from .models import *
# from django.http import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework import mixins
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets
# from django.shortcuts import get_object_or_404
# from django.views.generic.base import View
# import json
# from datetime import date
# Create your views here.

from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
import jwt
from .models import *
import json
from datetime import datetime, timedelta



class LoginAPI(APIView):

    def post(self, request):
        JWT_SECRET = 'HarryMaguire'
        JWT_ALGORITHM = 'HS256'
        JWT_EXP_DELTA_SECONDS = 2628000
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
            
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            
            return Response({"status": "200 OK", "username": username, "token": jwt_token})
        else:
            return Response({"status": "400 Bad Request", "message": "Invalid Password/Username"})

class RegisterAPI(APIView):
    def post(self, request):
        JWT_SECRET = 'HarryMaguire'
        JWT_ALGORITHM = 'HS256'
        JWT_EXP_DELTA_SECONDS = 2628000
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        fname = request.data['fname']
        lname = request.data['lname']
        
        try:
            user = User.objects.create_user(username, email, password, first_name=fname,last_name=lname)
            user.save()
            try:
                payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
            
                jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                
                return Response({"status": "200 OK", "username": username, "fname": fname, "lname": lname, "email": email, "token": jwt_token})
            except:
                return Response({"status": "400 Bad Request", "message": "Invalid Password/Username"})
        except:
            return Response({"status": "403 User already exists", "message": "User already exists."})
    
class ProfileAPI(APIView):
    def get(self, request, username):
        try:
            thatUser = User.objects.filter(username=username)[0]
            print(thatUser.first_name)
            resp = {
                "status": "200 OK",
                "username": username,
                "first_name": thatUser.first_name,
                "last_name": thatUser.last_name,
                "email": thatUser.email
            }
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})
        
    def put(self, request, username):
        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            User.objects.filter(username=username).update(email=email, first_name=first_name, last_name=last_name)
            thatUser = User.objects.filter(username=username)[0]
            resp = {
                "status": "200 OK",
                "message": "successfully updated.",
                "username": username,
                "first_name": thatUser.first_name,
                "last_name": thatUser.last_name,
                "email": thatUser.email
            }
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})