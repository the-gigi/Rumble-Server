from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from server import get_instance


class User(Resource):
    def get(self):
        return dict(result='OK')
    def post(self):
        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('handle', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        server = get_instance()
        server.register(**args)
        return dict(result='OK')


class LoggedInUser(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        server = get_instance()
        user_auth = server.login(**args)
        return dict(user_auth=user_auth)


class RoomMember(Resource):
    def post(self):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        server = get_instance()
        args['user_auth'] = request.headers['Authorization']
        server.join_room(**args)

    def delete(self, name):
        user_auth = request.headers['Authorization']
        server = get_instance()
        server.leave_room(user_auth=user_auth, name=name)


class RoomMembers(Resource):
    def get(self, name):
        user_auth = request.headers['Authorization']
        server = get_instance()
        result = server.get_room_members(user_auth=user_auth, name=name)
        return dict(result=result)


class Room(Resource):
    def post(self, name):
        user_auth = request.headers['Authorization']
        server = get_instance()
        server.create_room(user_auth=user_auth, name=name)

    def delete(self, name):
        user_auth = request.headers['Authorization']
        server = get_instance()
        server.destroy_room(user_auth=user_auth, name=name)

class Rooms(Resource):
    def get(self):
        user_auth = request.headers['Authorization']
        server = get_instance()
        return dict(result=server.get_rooms(user_auth=user_auth))

class Message(Resource):
    def post(self, name):
        user_auth = request.headers['Authorization']
        parser = RequestParser()
        parser.add_argument('message', type=str, required=True)
        message = parser.parse_args()['message']
        server = get_instance()
        server.handle_message(user_auth, name, message)

class Messages(Resource):
    def get(self, name, start, end):
        user_auth = request.headers['Authorization']
        server = get_instance()
        result = server.get_messages(user_auth, name, start, end)
        result = {k.isoformat(): v for k,v in result.iteritems()}
        return dict(result=result)




