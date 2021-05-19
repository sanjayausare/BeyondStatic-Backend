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

class LoginAPI(APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token = ""
            return Response({"status": "200 OK", "username": username, "token": token})
        else:
            return Response({"status": "400 Bad Request", "message": "Invalid Password/Username"})
        

class RegisterAPI(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        fname = request.data['fname']
        lname = request.data['lname']
        
        try:
            user = User.objects.create_user(username, email, password, first_name=fname,last_name=lname)
            user.save()
            try:
                token = ""
                return Response({"status": "200 OK", "username": username, "fname": fname, "lname": lname, "email": email, "token": token})
            except:
                return Response({"status": "400 Bad Request", "message": "Invalid Password/Username"})
        except:
            return Response({"status": "500 Internal Server Error", "message": "Some error on server side."})
    
        