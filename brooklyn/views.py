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
        
class ProjectAPI(APIView):
    def post(self, request, username):
        try:
            user = User.objects.filter(username=username)[0]
            ProjectName = request.data['ProjectName']
            EndpointURL = request.data['EndpointURL']
            Field1Name = request.data['Field1Name']
            Field2Name = request.data['Field2Name']
            Field3Name = request.data['Field3Name']
            Field4Name = request.data['Field4Name']
            Field5Name = request.data['Field5Name']
            
            try:
                addProj = Project(user=user, ProjectName=ProjectName, EndpointURL=EndpointURL, Field1Name=Field1Name, Field2Name=Field2Name, Field3Name=Field3Name, Field4Name=Field4Name, Field5Name=Field5Name)
                addProj.save()
            except:
                return Response({"status": "500 Internal Server Error", "message": "database went through an error."})
            
            resp = {
                "username": addProj.user.username,
                "id": addProj.id,
                "ProjectName": addProj.ProjectName,
                "EndpointURL": addProj.EndpointURL,
                "Field1Name": addProj.Field1Name,
                "Field2Name": addProj.Field2Name,
                "Field3Name": addProj.Field3Name,
                "Field4Name": addProj.Field4Name,
                "Field5Name": addProj.Field5Name,
            }
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})
        
    def get(self, request, username):
        try:
            thisUser = User.objects.filter(username=username)[0]
            requiredProjects = Project.objects.filter(user=thisUser)
            resp = []
            for reqProject in requiredProjects:
                respo = {
                    "id": reqProject.id,
                    "ProjectName": reqProject.ProjectName,
                    "EndpointURL": reqProject.EndpointURL,
                    "Field1Name": reqProject.Field1Name,
                    "Field2Name": reqProject.Field2Name,
                    "Field3Name": reqProject.Field3Name,
                    "Field4Name": reqProject.Field4Name,
                    "Field5Name": reqProject.Field5Name,
                }
                resp.append(respo)
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})