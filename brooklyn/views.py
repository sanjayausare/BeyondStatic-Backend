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
import pytz
from django.http import HttpResponse, HttpResponseRedirect
utc=pytz.UTC

def validateJWT(request):
    jwtToken = request.META['HTTP_AUTHORIZATION']
    try:
        validation = jwt.decode(jwtToken, 'HarryMaguire', algorithms="HS256")
        return True
    except:
        return False
    
class TokenCheckAPI(APIView):
    
    def post(self, request):
        token = request.data['token']
        try:
            validation = jwt.decode(token, 'HarryMaguire', algorithms="HS256")
            return Response({"status": True})
        except:
            return Response({"status": False})
        
class LoginAPI(APIView):

    def post(self, request):
        JWT_SECRET = 'HarryMaguire'
        JWT_ALGORITHM = 'HS256'
        # JWT_EXP_DELTA_SECONDS = 2628000
        JWT_EXP_DELTA_SECONDS = 2628000
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = {
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
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
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
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            if len(User.objects.filter(username=username)) == 0:
                return Response({"status": "404 Not Found", "message": "username does not exist."})
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
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            user = User.objects.filter(username=username)[0]
            ProjectName = request.data['ProjectName']
            EndpointURL = request.data['EndpointURL']
            Field1Name = request.data['Field1Name']
            Field2Name = request.data['Field2Name']
            Field3Name = request.data['Field3Name']
            Field4Name = request.data['Field4Name']
            Field5Name = request.data['Field5Name']
            Description = request.data['Description']
            
            try:
                addProj = Project(user=user, ProjectName=ProjectName, EndpointURL=EndpointURL, Field1Name=Field1Name, Field2Name=Field2Name, Field3Name=Field3Name, Field4Name=Field4Name, Field5Name=Field5Name, Description=Description)
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
                "Description": addProj.Description,
                "ProjectStatus": addProj.ProjectStatus
            }
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})
        
    def get(self, request, username):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            thisUser = User.objects.filter(username=username)[0]
            requiredProjects = Project.objects.filter(user=thisUser)
            resp = []
            for reqProject in requiredProjects:
                try:
                    totalMessages = len(ProjectObject.objects.filter(Project=reqProject))
                except:
                    totalMessages = 0
                respo = {
                    "id": reqProject.id,
                    "username": reqProject.user.username,
                    "ProjectName": reqProject.ProjectName,
                    "EndpointURL": reqProject.EndpointURL,
                    "Field1Name": reqProject.Field1Name,
                    "Field2Name": reqProject.Field2Name,
                    "Field3Name": reqProject.Field3Name,
                    "Field4Name": reqProject.Field4Name,
                    "Field5Name": reqProject.Field5Name,
                    "Description": reqProject.Description,
                    "ProjectStatus": reqProject.ProjectStatus,
                    "totalMessages": totalMessages
                }
                resp.append(respo)
            return Response(resp)
        except:
            return Response({"status": "404 Not Found", "message": "username does not exist."})
        
class ProjectInstanceAPI(APIView):
    def get(self, request, id):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            reqProject = Project.objects.filter(id=id)[0]
        except:
            return Response({"status": "404 Not Found", "message": "project does not exist."})
        try:
            totalMessages = len(ProjectObject.objects.filter(Project=reqProject))
        except:
            totalMessages = 0
        resp = {
            "id": reqProject.id,
            "ProjectName": reqProject.ProjectName,
            "username": reqProject.user.username,
            "EndpointURL": reqProject.EndpointURL,
            "Field1Name": reqProject.Field1Name,
            "Field2Name": reqProject.Field2Name,
            "Field3Name": reqProject.Field3Name,
            "Field4Name": reqProject.Field4Name,
            "Field5Name": reqProject.Field5Name,
            "ProjectStatus": reqProject.ProjectStatus,
            "Description": reqProject.Description,
            "totalMessages": totalMessages
        }
        return Response(resp)
    
    def put(self, request, id):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        if (len(Project.objects.filter(id=id))) == 0:
            return Response({"status": "404 Not Found", "message": "project does not exist."})
        ProjectName = request.data['ProjectName']
        EndpointURL = request.data['EndpointURL']
        Field1Name = request.data['Field1Name']
        Field2Name = request.data['Field2Name']
        Field3Name = request.data['Field3Name']
        Field4Name = request.data['Field4Name']
        Field5Name = request.data['Field5Name']
        Description = request.data['Description']
        ProjectStatus = request.data['ProjectStatus']
        Project.objects.filter(id=id).update(Description=Description, ProjectStatus=ProjectStatus, ProjectName=ProjectName, EndpointURL=EndpointURL, Field1Name=Field1Name, Field2Name=Field2Name, Field3Name=Field3Name, Field4Name=Field4Name, Field5Name=Field5Name)
        reqProject = Project.objects.filter(id=id)[0]
        resp = {
            "id": reqProject.id,
            "ProjectName": reqProject.ProjectName,
            "username": reqProject.user.username,
            "EndpointURL": reqProject.EndpointURL,
            "Field1Name": reqProject.Field1Name,
            "Field2Name": reqProject.Field2Name,
            "Field3Name": reqProject.Field3Name,
            "Field4Name": reqProject.Field4Name,
            "Field5Name": reqProject.Field5Name,
            "Description": reqProject.Description,
            "ProjectStatus": reqProject.ProjectStatus
        }
        return Response(resp)
    
    def delete(self, request, id):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        if (len(Project.objects.filter(id=id))) == 0:
            return Response({"status": "404 Not Found", "message": "project does not exist."})
        try:
            Project.objects.filter(id=id).delete()
            return Response({"status": "202 Accepted", "message": "project deleted successfully."})
        except:
            return Response({"status": "500 Internal Server Error", "message": "database error."})
        
class AddInstanceAPI(APIView):
    def get(self, request, message):
        message = message.split('zlatan')
        decryptedMessage = []
        for m in message:
            mess = ""
            chunks = [m[i:i+4] for i in range(0, len(m), 4)]
            for chunk in chunks:
                mess += chr(int(chunk))
            decryptedMessage.append(mess)
        
        username = decryptedMessage[0]
        projectID = int(decryptedMessage[1])
        field1 = decryptedMessage[2]
        field2 = decryptedMessage[3]
        field3 = decryptedMessage[4]
        field4 = decryptedMessage[5]
        field5 = decryptedMessage[6]
        
        try:
            user = User.objects.filter(username=username)[0]
            print(user.username)
            Project2 = Project.objects.filter(id=projectID)[0]
            
            if Project2.ProjectStatus is False:
                return HttpResponseRedirect(Project2.EndpointURL)
        except:
            #incorrect user/project
            return Response({"status": "404 Not Found", "message": "project/user does not exist."})
        
        try:
            newProjectObjectInstance = ProjectObject(Project=Project2, user=user, Field1=field1, Field2=field2, Field3=field3, Field4=field4, Field5=field5)
            newProjectObjectInstance.save()
        except:
            #ServerError
            return HttpResponseRedirect(Project2.EndpointURL)
        
        endpoint = Project2.EndpointURL
        
        return HttpResponseRedirect(endpoint)
    

class ProjectObjectsAPI(APIView):
    def get(self, request, projectID):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            thatProject = Project.objects.filter(id=projectID)[0]
        except:
            return Response({"status": "404 Not Found", "message": "project does not exist."})
        allObjectInstances = ProjectObject.objects.filter(Project=thatProject)
        requiredInstances = []
        for objectInstance in allObjectInstances:
            resp = {
            "id": objectInstance.id,
            "ProjectID": objectInstance.Project.id,
            "UserID": objectInstance.user.username,
            "Field1": objectInstance.Field1,
            "Field2": objectInstance.Field2,
            "Field3": objectInstance.Field3,
            "Field4": objectInstance.Field4,
            "Field5": objectInstance.Field5,
            "dateTime": str(objectInstance.DateTime)
            }
            requiredInstances.append(resp)
        return Response(requiredInstances)
    
class ProjectObjectAPI(APIView):
    def get(self, request, projectobjectID):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            thatProjectObject = ProjectObject.objects.filter(id=projectobjectID)[0]
        except:
            return Response({"status": "404 Not Found", "message": "project object does not exist."})
        resp = {
            "id": thatProjectObject.id,
            "projectID": thatProjectObject.Project.id,
            "username": thatProjectObject.user.username,
            "field1": thatProjectObject.Field1,
            "field2": thatProjectObject.Field2,
            "field3": thatProjectObject.Field3,
            "field4": thatProjectObject.Field4,
            "field5": thatProjectObject.Field5,
            "dateTime": str(thatProjectObject.DateTime)
        }
        return Response(resp)
    
    def delete(self, request, projectobjectID):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        if len(ProjectObject.objects.filter(id=projectobjectID)) == 0:
            return Response({"status": "404 Not Found", "message": "project object does not exist."})
        try:
            ProjectObject.objects.filter(id=projectobjectID).delete()
            return Response({"status": "202 Accepted", "message": "project object deleted successfully."})
        except:
            return Response({"status": "500 Internal Server Error", "message": "database went through an error."})
        
class AllMessagesCountAPI(APIView):
    def get(self, request, username):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        try:
            thisUser = User.objects.filter(username=username)[0]
            try:
                totalMessages = len(ProjectObject.objects.filter(user=thisUser))
            except:
                totalMessages = 0
            return Response({"status": "200 OK", "totalMessageCount": totalMessages})
        except:
            return Response({"status": "404 Not Found", "message": "User does not exist"})
        
class ChartDataAPI(APIView):
    def get(self, request, username):
        if validateJWT(request) is False:
            return Response({"status": "401 Unauthorized", "message": "authentication token invalid."})
        
        # get all instances
        #try:    
        thisUser = User.objects.filter(username=username)[0]
        allMessages = ProjectObject.objects.filter(user=thisUser)
        xAxis = ["1", "2", "3", "4", "5", "6"]
        currentDateTime = datetime.now()
        dt1 = currentDateTime - timedelta(30*6)
        dt2 = currentDateTime - timedelta(30*5)
        dt3 = currentDateTime - timedelta(30*4)
        dt4 = currentDateTime - timedelta(30*3)
        dt5 = currentDateTime - timedelta(30*2)
        dt6 = currentDateTime - timedelta(30*1)
        
        dt1 = utc.localize(dt1).replace(tzinfo=utc)
        dt2 = utc.localize(dt2).replace(tzinfo=utc)
        dt3 = utc.localize(dt3).replace(tzinfo=utc)
        dt4 = utc.localize(dt4).replace(tzinfo=utc)
        dt5 = utc.localize(dt5).replace(tzinfo=utc)
        dt6 = utc.localize(dt6).replace(tzinfo=utc)
        currentDateTime = utc.localize(currentDateTime).replace(tzinfo=utc)
        
        c1=0
        c2=0
        c3=0
        c4=0
        c5=0
        c6=0
        for message in allMessages:
            if(message.DateTime>=dt1 and message.DateTime<=dt2):
                c1 += 1
            elif (message.DateTime>=dt2 and message.DateTime<=dt3):
                c2 += 1
            elif (message.DateTime>=dt3 and message.DateTime<=dt4):
                c3 += 1
            elif (message.DateTime>=dt4 and message.DateTime<=dt5):
                c4 += 1
            elif (message.DateTime>=dt5 and message.DateTime<=dt6):
                c5 += 1
            elif (message.DateTime>=dt6 and message.DateTime<=currentDateTime):
                c6 += 1
        yAxis = [c1, c2, c3, c4, c5, c6]
        return Response({"status": "200 OK", "xAxis": xAxis, "yAxis": yAxis})
        #except:
        #    return Response({"status": "404 Not Found", "message": "User does not exist"})