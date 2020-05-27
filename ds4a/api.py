from flask import Flask
from flask_restful import Resource, Api
#import dash
#import dash_html_components as html

app = Flask(__name__)

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Planify(Resource):
    def get(self):
        return 'Planify API'

class DailyDrivers(Resource):
    def get(self):
        return 'API expects params date and number of steps ahead'

class DailyDriversFor(Resource):

    def get(self, date, steps):
        return {'prediction': 'here goes {} number of prediction from {}'.format(steps, date)}

api.add_resource(Planify, '/')
api.add_resource(HelloWorld, '/hello')
api.add_resource(DailyDrivers, '/daily-drivers')
api.add_resource(DailyDriversFor, '/daily-drivers/<date>/<steps>')


if __name__ == '__main__':
    app.run(debug=True)