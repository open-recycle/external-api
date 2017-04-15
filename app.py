
# coding: utf8
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
import logging
from map_utils import getDistance
#try:
from classify import run_inference_on_image
import os
#except:
#    pass

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NearWastePlace(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('class', type=str, help='Class of shared waste')
            parser.add_argument('latitude', type=str, help='Class of shared waste')
            parser.add_argument('longitude', type=str, help='Class of shared waste')
            args = parser.parse_args()
            _class = args['class']
            _latitude = args['latitude']
            _longitude = args['longitude']

            print(_latitude)
            print(_longitude)

            with codecs.open("place-waste.csv", encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                i = 0
                db_place = []
                for row in reader:
                    if i > 0:
                        db_id = i
                        db_country = 'Россия'
                        db_city = row[0]
                        db_metro = row[1]
                        db_region_city = row[1]
                        db_latitude = row[2][:row[2].index(',')]
                        db_longitude = row[2][row[2].index(',') + 1:]
                        db_address = row[3]
                        db_schedule = row[4]
                        db_comment = 'Комментарий'
                        db_social = row [5]
                        db_place.append({
                            'id': db_id,
                            'country' : db_country,
                            'city' : db_city,
                            'metro' : db_metro,
                            'region_city' : db_region_city,
                            'latitude' : db_latitude,
                            'longitude': db_longitude ,
                            'address' : db_address,
                            'schedule' : db_schedule,
                            'comment' : db_comment,
                            'social'  : db_social
                        })
                    i += 1
                    pass

            place_list = getDistance(origin=_latitude+","+_longitude,coordinate=None, csvf="place-waste.csv",sqlitef=None)
            print(place_list)

            near_place = []
            other_place = []
            id_list = []
            for rec in place_list[1]:
                id_list.append(rec[0])
                pass

            print (id_list)
            print ("**1**")
            for rec in db_place:
                print (rec['id'])
                if rec['id'] in id_list:
                    print ("---1")
                    for obj in place_list[1]:
                        print (obj)
                        if obj[0] == rec['id']:
                            dist=obj[1]
                    print (dist)
                    #print (place_list[1] [x for i in id_list if x == rec['id']])
                    print ("---1-")
                    near_place.append({'place': rec, 'distance': dist})
                else:
                    print ("---2")
                    other_place.append({'place':rec})
            print ("4--")
            """
            placeitems: {
            country:
            city:
            metro:
            place:
            latitude:
            longitude:
            address:
            schedule:
            comment:
            social:
            }
            """
            print ('result')
            return {'StatusCode': '200', 'Message': 'Operation successful', 'NearPlace': near_place, 'OtherPlace':other_place}
            pass
        except Exception as e:
            return {'error': str(e)}
            pass

class CollectionsPoint(Resource):
    def post(self):
        try:
            # Parse the arguments
            print ("1")
            parser = reqparse.RequestParser()
            print ("2")
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
                i = 0
                for row in reader:
                    if i>0:
                        if ((_metro in row[1].split(',') or _district in row[1].split(',')) or
                            (_metro == "" and _district == "")):
                                db_id = i
                                db_country = 'Россия'
                                db_city = row[0]
                                db_metro = row[1]
                                db_region_city = row[1]
                                db_latitude = row[2][:row[2].index(',')]
                                db_longitude = row[2][row[2].index(',') + 1:]
                                db_address = row[3]
                                db_schedule = row[4]
                                db_comment = 'Комментарий'
                                db_social = row[5]
                                result.append({
                                    'id': db_id,
                                    'country': db_country,
                                    'city': db_city,
                                    'metro': db_metro,
                                    'region_city': db_region_city,
                                    'latitude': db_latitude,
                                    'longitude': db_longitude,
                                    'address': db_address,
                                    'schedule': db_schedule,
                                    'comment': db_comment,
                                    'social': db_social
                                })
                    i += 1

            return {'StatusCode':'200','Message': 'Operation successful', 'Places':result}
        except Exception as e:
            return {'error': str(e)}

class UploadFile4Recognition(Resource):
    def put(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, help='user_id')
            parser.add_argument('filename',type=str, help='Class of shared waste')
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', help='Class of shared waste')
            args = parser.parse_args()
            print(args)
            _userid = args['user_id']
            _filename = args['filename']
            _file = args['file'].stream

            request_id = uuid.uuid1().__str__()
            fn = "[{}]-[{}]-[{}]-{}".format(request_id,_userid,time.time(),_filename)+".jpg"
            full_fn = "files4recognition"+os.sep+fn
            with open(full_fn,'wb') as fout:
                fout.write(_file.getvalue())
            fout.close()
            resultFlag = True
            #
            #
            resp = "сеть скорей всего не работает. печаль!!!"
            print (full_fn)
            try:
                resp = run_inference_on_image(full_fn)
                print ("--->",resp)
            except Exception as e:
                resultFlag = False
                print (e)
            #
            #
            #
            result = ''
            try:
                with codecs.open("recycle_db.csv", encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for rec in reader:
                        if rec[2] in resp or resp in rec[2]:
                            result = rec[1]
                if result == '':
                    result = "unknown type of waste"
                pass
            except Exception as e:
                print (e)
                if 'disposable paper cups resize' in resp:
                    result = "бумажный стакан"
                if 'lame foil' in resp:
                    result = "фольга"
                if 'glass bottle' in resp:
                    result = "стеклянная бутылка"
                if 'plastic bottle' in resp:
                    result = "пластиковая бутылка"
                if 'stupid' in resp:
                    result = "неудалось определить класс отходов"
                if 'receipt' in resp:
                    result = "чек"
                if 'aluminium cup' in resp:
                    result = "aluminium cup"
                #result = result.encode('utf-8')
                print("++++",result)
                pass

            return {'StatusCode': '200', 'Message': result, 'callback_id' : request_id}
        except Exception as e:
            return {'error': str(e)}

class GetList(Resource):
    def get(self):
        db_list=[]
        with codecs.open("recycle_db.csv", encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for rec in reader:
                db_list.append({'id':rec[0],'name_rus':rec[1],'name_eng':rec[2]})
        return {'StatusCode':'200', 'Message':db_list}

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
    def post(self):
        try:
            # Parse the arguments
            print ("1")
            parser = reqparse.RequestParser()
            print ("2")
            parser.add_argument('user_id', type=str, help='user_id')
            parser.add_argument('source',  type=str, help='user_id')
            parser.add_argument('filename', type=str, help='filename')
            parser.add_argument('descr', type=str, help='descr')
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', help='Class of shared waste')
            args = parser.parse_args()
            print(args)
            _userid = args['user_id']
            _source = args['source']
            _descr = args['descr']
            _filename = args['filename']
            _file = args['file'].stream

            print(args)

            if _source == 'bot':
                filename = "files4learning"+os.sep+_filename
            else:
                filename = "files4learning"+os.sep+"{}-{}-{}-{}".format(_descr, _userid, time.time(), _filename)
            with open(filename,'wb') as fout:
                fout.write(_file.getvalue())
            fout.close()
            return {'StatusCode':'200','Message': 'File saved'}

        except Exception as e:
            print (e)
            return {'error': str(e)}

api.add_resource(CollectionsPoint, '/api/CollectionsPoint')
api.add_resource(UploadFile4Recognition, '/api/UploadFile4Recognition')
api.add_resource(UploadFile4Learn, '/api/UploadFile4Learning')
api.add_resource(GetTaskResult, '/api/CallBack')
api.add_resource(GetList, '/api/List')
api.add_resource(NearWastePlace, '/api/NearWastePlace')


@app.route("/")
def hello():
    return "Welcome to API for Open Recycle Community!"

app.config['PROFILE'] = True
#app.config['SERVER_NAME'] = '0.0.0.0'
app.config['TRAP_HTTP_EXCEPTIONS'] = True

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=48777)
