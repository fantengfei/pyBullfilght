# -*- coding: utf-8 -*-
"""
    play namespace
    ~~~~~~
    :copyright: (c) 2017 by Taffy.
"""

from flask_socketio import SocketIO, Namespace, send, emit, join_room, leave_room, rooms
from flask import request
import check
import json

class PlayNamespace(Namespace):
    
    playrooms = {}
    clients = {}

    '''
        join room
        
        append `room: user` info to playrooms
        append `sesstion: sid` to clients
    '''
    def on_join(self, data):
        user = data['user']
        room = data['room']
        
        # get users from room
        users = self.playrooms.get(room, [])
        inRoom = False

        for u in users:
            if u['openid'] == user['openid']:
                inRoom = True
                break
        
        # not in user list
        if inRoom == False:
            users.append(user)
            self.playrooms[room] = users

        # leave room for invalid sid
        leave_room(room, self.clients.get(user['openid']))

        # save sid
        self.clients[user['openid']] = request.sid
            
        # join room
        join_room(room)

        print str(self.playrooms.keys())
        
        emit('join', users, room = room)


    '''
        leave room

        pop `sid` from clients
        pop `user` from playrooms
    '''
    def on_leave(self):

        session = list(self.clients.keys())[self.clients.values().index(request.sid)]

        for k, v in self.playrooms.items():
            for u in v:
                if u['openid'] == session:
                    room = k 
                    user = u
                    break
            if room:
                self.clients.pop(session)
                self.playrooms.pop(room)
                break

        if room:
            leave_room(room)

        print user['nickName'] + ' leave ' + room

        emit('leave', user, room = room)
        
                
        