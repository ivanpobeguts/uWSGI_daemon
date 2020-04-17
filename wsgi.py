import re
import json
import urllib2


def application(environ, start_response):
    ip = parse_request(environ)
    if ip:
        city = get_city_by_ip(ip)
        weather_dict = get_weather_by_city(city)
        if city and weather_dict:
            weather_dict.update({'city': city})
            start_response('200 OK', [('Content-Type', 'application/json')])
            json.dumps(weather_dict)
            return [json.dumps(weather_dict)]
    start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
    return ['<h1>Not Found</h1>']


def parse_request(environ):
    if environ.get('REQUEST_METHOD') == 'GET':
        try:
            request_regex = re.compile(r'^/(?P<path>.*)/(?P<ip>(\d+\.\d+\.\d+\.\d+))$')
            request_path = request_regex.match(environ.get('REQUEST_URI'))
            if request_path.group('path') == 'ip2w':
                ip = request_path.group('ip')
                return ip
        except AttributeError:
            pass


def get_city_by_ip(ip, token='c4e68c980d8067'):
    try:
        raw_response = urllib2.urlopen('https://ipinfo.io/{}?token={}'.format(ip, token))
        response = json.loads(raw_response.read())
        return response.get('city')
    except urllib2.HTTPError:
        pass


def get_weather_by_city(city, token='bd0708efda82a2e1244cbd555c349f02'):
    result = {}
    try:
        raw_response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, token))
        response = json.loads(raw_response.read())
        result['conditions'] = response['weather'][0]['description']
        result['temp'] = response['main']['temp']
    except KeyError, urllib2.HTTPError:
        pass
    return result


