import json
import boto3
from pymongo import MongoClient
import dns.resolver
import dns.query
from bson import ObjectId
import ast
import jwt

def lambda_handler(event, context):
    val = jwt_validate(event)
    if val is not True:
        return val
    collection = get_collection()
    theJSON = event['body']
    thatMail = theJSON['email']
    try:
        collection.find_one_and_update({"email": thatMail}, {"$set": theJSON})
    except:
        errorCode = {
            "error": 407,
            "message": "some error occurred."
        }
        return errorCode
    try:
        list_cur = list(collection.find({"email": thatMail}))[0]
        list_cur = getInstanceJSON(list_cur)
        list_cur = ast.literal_eval(list_cur)
        del list_cur['_id']
        del list_cur['password']
    except:
        errorCode = {
            "error": 407,
            "message": "email doesnt exist."
        }
        return errorCode
    data = list_cur
    success = {
        "code": 200,
        "status": "OK",
        "data": data
    }
    return success

def jwt_validate(event):
    jwtToken = event['headers']['Authorization']
    if jwtToken[:6] != 'Bearer':
        errorCode = {
            "code": 403,
            "status": "forbidden"
        }
        return errorCode
    jwtToken = jwtToken.split()[1]
    try:
        jwt.decode(jwtToken, 'techcurve', algorithms=["HS256"])
        return True
    except:
        errorCode = {
            "code": 403,
            "status": "forbidden"
        }
        return errorCode

def getInstanceJSON(list_cur):
    return JSONEncoder().encode(list_cur)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_collection():
    s3 = boto3.resource('s3')

    content_object = s3.Object('vitp', 'config.json')
            
    file_content = content_object.get()['Body'].read().decode('utf-8')
    DBdata = json.loads(file_content)
    connection_string = DBdata['connection_string']
    cluster = MongoClient(connection_string)
    db = cluster['virtualITTraining']
    collection = db['student']
        
    return collection