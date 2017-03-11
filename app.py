from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import werkzeug
from io import StringIO
import time
import uuid
import codecs
import csv
import json

app = Flask(__name__)
api = Api(app)

class CollectionsPoint(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('class', type=str, help='Class of shared waste')
            parser.add_argument('district', type=str, help='A district of the city')
            parser.add_argument('metro', type=str, help='Metro')
            args = parser.parse_args()

            _class = args['class']
            _district = args['district']
            _metro = args['metro']

            result = []
            with codecs.open("place-waste.csv", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in reader:
                    if row[0] != 'point':
                        if _metro in row[0].split(',') or _district in row[0].split(','):
                            result.append(row)
                        pass
            return {'StatusCode':'200','Message': 'Operation successful', 'Place':result}
        except Exception as e:
            return {'error': str(e)}

class UploadFile4Recognition(Resource):
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id',required=True, type=str, help='user_id')
            parser.add_argument('filename',required=True, type=str, help='Class of shared waste')
            parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files', help='Class of shared waste')
            args = parser.parse_args()
            _userid = args['user_id']
            _filename = args['filename']
            _file = args['file'].stream

            request_id = uuid.uuid1().__str__()

            with open("files4recognition/[{}]-[{}]-[{}]-{}".format(request_id,_userid,time.time(),_filename),'wb') as fout:
                fout.write(_file.getvalue())
            fout.close()

            return {'StatusCode': '2001', 'Message': 'File unsaved', 'callback_id' : request_id}
        except Exception as e:
            return {'error': str(e)}

class GetTaskResult(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('task_id',required=True, type=str, help='user_id')
            args = parser.parse_args()
            _taskid = args['task_id']

            return {'StatusCode': '200', 'Message': _taskid}
        except Exception as e:
            return {'error': str(e)}

class UploadFile4Learn(Resource):
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id',required=True, type=str, help='user_id')
            parser.add_argument('filename',required=True, type=str, help='filename')
            parser.add_argument('descr', required=True, type=str, help='descr')
            parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files', help='Class of shared waste')
            args = parser.parse_args()
            _userid = args['user_id']
            _descr = args['descr']
            _filename = args['filename']
            _file = args['file'].stream

            with open("files4learning/{}-{}-{}-{}".format(_descr,_userid,time.time(),_filename),'wb') as fout:
                fout.write(_file.getvalue())
            fout.close()

            return {'StatusCode':'200','Message': 'File saved'}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CollectionsPoint, '/api/CollectionsPoint')
api.add_resource(UploadFile4Recognition, '/api/UploadFile4Recognition')
api.add_resource(UploadFile4Learn, '/api/UploadFile4Learning')
api.add_resource(GetTaskResult, '/api/CallBack')

@app.route("/")
def hello():
    return "Welcome to API for Open Recycle Community!"

if __name__ == '__main__':
    app.run(debug=True)