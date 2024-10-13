#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session['user_id']).first()
        
        if user:
            return user.to_dict(), 200
        return {}, 204

class Login(Resource):
    def post(self):
        username = request.json['username']
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {
            "message": "Invalid Credentials"
        }, 401

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {
            "message": "204: resource deleted"
        }, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')




if __name__ == '__main__':
    app.run(port=5555, debug=True)
