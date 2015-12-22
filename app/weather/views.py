#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, send_file
import datetime
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
import urllib2
import sys
import os
import json
from .config import *
from ..models import *
from ..lib.util import *
sys.path.append('..')


def isValid(data):
    flag = 0
    for key in data.keys():
        if data[key] == 99999:
            flag += 1
    if flag == 0:
        return True
    return False


def isData(data):
    if data == 99999:
        return False
    else:
        return True


def wind_direct(wind_direction):
    wind_direct = None
    if 22.6 <= float(wind_direction) and float(wind_direction) <= 67.5:
        wind_direct = '东北'
    if 67.6 <= float(wind_direction) and float(wind_direction) <= 112.5:
        wind_direct = '东'
    if 112.6 <= float(wind_direction) and float(wind_direction) <= 157.5:
        wind_direct = '东南'
    if 157.6 <= float(wind_direction) and float(wind_direction) <= 202.5:
        wind_direct = '南'
    if 202.6 <= float(wind_direction) and float(wind_direction) <= 247.5:
        wind_direct = '西南'
    if 247.6 <= float(wind_direction) and float(wind_direction) <= 292.5:
        wind_direct = '西'
    if 292.6 <= float(wind_direction) and float(wind_direction) <= 337.5:
        wind_direct = '西北'
    if 337.6 <= float(wind_direction) or float(wind_direction) <= 22.5:
        wind_direct = '北'
    return wind_direct


def wind_speed(wind_speed):
    wind_order = None
    if 0 <= float(wind_speed) <= 0.2:
        wind_order = 0
    if 0.3 <= float(wind_speed) <= 1.5:
        wind_order = 1
    if 1.6 <= float(wind_speed) <= 3.3:
        wind_order = 2
    if 3.4 <= float(wind_speed) <= 5.4:
        wind_order = 3
    if 5.5 <= float(wind_speed) <= 7.9:
        wind_order = 4
    if 8.0 <= float(wind_speed) <= 10.7:
        wind_order = 5
    if 10.8 <= float(wind_speed) <= 13.8:
        wind_order = 6
    if 13.9 <= float(wind_speed) <= 17.1:
        wind_order = 7
    if 17.2 <= float(wind_speed) <= 20.7:
        wind_order = 8
    if 20.8 <= float(wind_speed) <= 24.4:
        wind_order = 9
    if 24.5 <= float(wind_speed) <= 28.4:
        wind_order = 10
    if 28.5 <= float(wind_speed) <= 32.6:
        wind_order = 11
    return wind_order


class realWether(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('sitenumber', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('rain', type=str)
        parser.add_argument('wind_direction')
        parser.add_argument('wind_speed')
        parser.add_argument('visibility', type=str)
        parser.add_argument('humi', type=str)
        parser.add_argument('pressure', type=str)
        args = parser.parse_args(strict=True)
        record = reltiWeather(args['datetime'], args['name'],
                              args['sitenumber'], args['tempe'],
                              args['humi'], args['wind_direction'],
                              args['wind_speed'], args['pressure'],
                              args['rain'], args['visibility'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': "添加数据失败"}, 200
        return {'mesg': "添加数据成功!"}, 200


class realAqi(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('aqi', type=str)
        parser.add_argument('level')
        parser.add_argument('pripoll')
        parser.add_argument('content')
        parser.add_argument('measure')
        args = parser.parse_args(strict=True)
        record = reltiAqi(args['datetime'], args['aqi'], args['level'], args[
                          'pripoll'], args['content'], args['measure'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {"mesg": "添加数据失败!"}, 200
        return {'mesg': "添加数据成功!"}, 200


class foreWeat(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('view_time', type=str)
        parser.add_argument('direction', type=str)
        parser.add_argument('speed', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('weather', type=str)
        parser.add_argument('weatherpic', type=str)
        parser.add_argument('area', type=str)
        record = foreWeather(args['datetime'], args['view_time'],
                             args['direction'], args['speed'],
                             args['tempe'], args['weather'],
                             args['weatherpic'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': '数据添加失败!'}, 200
        return {'mesg': '数据添加成功!'}, 200


class wea_Station(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('site_name', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('rain', type=str)
        parser.add_argument('humi', type=str)
        parser.add_argument('air_press', type=str)
        parser.add_argument('wind_direction', type=str)
        parser.add_argument('wind_speed', type=str)
        parser.add_argument('vis', type=str)
        parser.add_argument('lon', type=str)
        parser.add_argument('lat', type=str)
        record = weaStation(args['datetime'], args['site_name'], args['tempe'],
                            args['rain'], args['humi'], args['air_press'],
                            args['wind_direction'], args['wind_speed'],
                            args['vis'], args['lon'], args['lat'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': '数据添加失败!'}
        return {'mesg': "数据添加成功!"}


class viewRelti(Resource):

    def get(self):
        area = request.args['area']
        time = request.args['time']
        record = reltiWeather.query.filter_by(
            reltiWeather.name == area
        ).order_by('datetime desc').limit(1)
        if record.id is None:
            return {'status': 'fail', "mesg": "数据缺失!"}
        aqi_record = reltiAqi.query().order_by('datetime desc').limit(1)
        data = {}
        data['tempe'] = record[0].tempe
        data['humi'] = record[0].humi
        data['pressure'] = record[0].pressure
        data['wind_direction'] = record[0].wind_direction
        data['wind_speed'] = record[0].wind_speed
        data['aqi'] = aqi_record[0].aqi
        data['level'] = aqi_record[0].level
        return {'status': 'success', "data": data}, 200


class viewForecast(Resource):

    def get(self):
        area = request.args['area']
        time = request.args['time']
        records = foreWeather.query.filter(
            foreWeather.view_time == datetime.datetime.now().strftime(
                '%Y-%m-%d'), area=area)
        if records.id is None:
            return {'status': 'fail', "mesg": "数据缺失"}
        data = []
        for record in records:
            temp = {}
            temp = to_json_list(record)
            del tempe['view_time']
            data.append(temp)
        return {'status': 'success', "data": data}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class alarm(Resource):

    def get(self):
        record = cityAlarm.query.order_by(cityAlarm.publishtime.desc()).first()
        if record is None:
            return {'status': 'fail', "mesg": "数据缺失"}
        data = to_json(record)
        del data['id']
        return {'status': 'success', "data": data}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('publishtime', type=str)
        parser.add_argument('type')
        parser.add_argument('level')
        parser.add_argument('content')
        args = parser.parse_args(strict=True)
        record = cityAlarm(args['publishtime'], args['type'],
                           args['level'], args['content'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': "上传数据失败!"}
        return {'mesg': '上传数据成功!'}

    def put(self):
        pass

    def delete(self):
        pass

type_codes = ['a', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
alarm_types = ['台风', '暴雨', '暴雪', '寒潮', '大风', '大雾', '雷电',
               '冰雹', '霜冻', '高温', '干旱', '道路结冰', '霾', '沙城暴', '臭氧']
alarm_levels = ['蓝色', '黄色', '橙色', '红色', '解除']
types = zip(alarm_types, type_codes)


class get_alarm(Resource):

    def get(self):
        response = urllib2.urlopen(url).read()
        response = json.loads(response)
        result = []
        for elem in response:
            if elem['level'] != '解除':
                level_code = alarm_levels.index(elem['level'])
                type_code = type_codes[alarm_types[elem['type']]]
                img_name = type_code + str(level_code)
                elem['img_name'] = img_name
            else:
                elem['img_name'] = None
                result.append(elem)
        return {'status': 'success', "data": result}


class alarm_img(Resource):
    def get(self):
        img_name = request.args['img_name']
        path = os.path.split(os.path.realpath(__file__))[0] + '/alarm_pic'
        img = os.path.join(path, img_name + '.jpg')
        return send_file(img)


class get_realtime(Resource):

    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(weather_url, headers=header)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)['data']
        temp = {}
        for dic in result:
            if dic['name'] == area:
                temp = dic
        if temp is None:
            return {'status': "fail", 'mesg': '该区域数据缺失!'}
        invalid_keys = ['sitenumber', 'rain', 'visibility']
        for key in invalid_keys:
            del temp[key]
        if not isData(temp['wind_speed']):
            temp['wind_speed'] = 0
        if not isData(temp['wind_direction']):
            temp['wind_direction'] = 0
        temp['wind_speed'] = str(wind_speed(temp['wind_speed'])) + '级'
        temp['wind_direction'] = wind_direct(
            temp['wind_direction']) + '风'
        aqi_req = urllib2.Request(aqi_url, headers=header)
        aqi_response = urllib2.urlopen(aqi_req).read()
        aqi = json.loads(aqi_response)['aqi']
        if aqi is None:
            return {'status': "fail", 'mesg': "aqi数据缺失!"}
        temp['aqi'] = aqi
        return {'status': 'success', "data": temp}


class get_forecast(Resource):

    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(forecast_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        return {'status': 'success', "data": response}


class get_rain(Resource):

    def get(self):
        lon = request.args['lon']
        lat = request.args['lat']
        rain_url = rain_pre + '&lon=' + str(lon) + '&lat=' + str(lat)
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(rain_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']['list']
        rain_list = []
        for elem in response:
            rain_list.append(elem['d'])
        if float(rain_list[0]) == 0:
            count = 0
            for i in range(len(rain_list)):
                if float(rain_list[i]) != 0:
                    count = i
                    break
            if count != 0:
                mesg = '当前位置没有雨,' + str(count * 6) + '分钟后降雨'
                return {'status': 'success', 'mesg': mesg}
            else:
                mesg = '当前位置没有雨，未来90分钟不会下雨'
                return {'status': 'success', 'mesg': mesg}
        else:
            count = 0
            for i in range(len(rain_list) - 1):
                if rain_list[i] < rain_list[i + 1]:
                    count += 1
            if count == 15:
                return {'status': 'success', 'mesg': '当前位置有雨, 未来90分钟累计降雨量为' +
                        str(rain_list[15]) + 'mm'}
            else:
                count = 0
                flag = False
                for i in range(len(rain_list) - 1):
                    for j in range(len(rain_list) - 1 - i):
                        if rain_list[i] == rain_list[j + i + 1]:
                            count = i
                            flag = True
                            break
                    if flag:
                        break
                mesg = '当前位置有雨, 未来' + \
                    str(count * 6) + '分钟降雨量为' + \
                    str(rain_list[count]) + 'mm, 之后雨停'
                return{'status': 'success', 'mesg': mesg}

import random
import math


def rad(arg):
    return float(arg) ** math.pi / 180


def distance(lat1, lng1, lat2, lng2):
    radlat1 = rad(lat1)
    radlat2 = rad(lat2)
    a = radlat1 - radlat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(radlat1) * math.cos(radlat2) * math.pow(math.sin(b / 2), 2)))
    earth_radius = 6378.137 * 1000
    s = s * earth_radius
    if s < 0:
        return -s
    else:
        return s


class get_qpf(Resource):

    def get(self):
        header = {'Accept': 'application/json',
                  'Content-Type': 'application/json'}
        request = urllib2.Request(rain_qpf, headers=header)
        response = urllib2.urlopen(request).read()
        records = json.loads(response)['data']
        '''
                        雨量预测测试
        '''
        for value in records:
            if distance('31.87', '121.33', value['lat'], value['lon']) < 100000:
                value['data'] = str(random.random())[:3]
        result = []
        for value in records:
            if value['data'] != 0:
                result.append(value)
        return {'status': 'success', 'data': result}


class autoStation(Resource):

    def get(self):
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(station_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']
        result = []
        for record in response:
            buf = {}
            location = site_infor.query.filter_by(
                site_name=record['site_name']).first()
            if location is not None:
                if wind_direct(record['wind_direction']) is not None and wind_speed(record['wind_speed']) is not None:
                    buf['longitude'] = location.longitude
                    buf['latitude'] = location.latitude
                    buf['tempe'] = record['tempe']
                    buf['rain'] = record['rain']
                    buf['wind_direction'] = wind_direct(
                        record['wind_direction']) + '风'
                    buf['wind_speed'] = str(
                        wind_speed(record['wind_speed'])) + '级'
                    buf['datetime'] = record['datetime']
                    result.append(buf)
        if result is None:
            return {'status': 'fail', 'mesg': '缺失数据!'}
        return {'mesg': '自动站信息', 'status': 'success', 'data': result}
