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
    thatMail = event['email']
    try:
        allStudents = list(collection.find({"email": thatMail}))[0]
        list_cur = getInstanceJSON(allStudents)
        list_cur = ast.literal_eval(list_cur)
        del list_cur['_id']
        del list_cur['password']
        if 'profilePicture' in list_cur.keys():
            list_cur['profilePicture'] = getImageLink(list_cur['profilePicture'])
        return list_cur
    except:
        errorCode = {
            "code": 409,
            "status": "email does not exist"
        }
        return errorCode

def getImageLink(name):
    bucket_name = 'vitp'
    object_name = name
    expiration = 3600
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

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