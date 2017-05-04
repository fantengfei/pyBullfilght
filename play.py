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
        if check.check_session(user['session']) == False:
            emit('join in', 'session 过期', json = False)
            return

        room = data['room']
        
        # get users from room
        users = self.playrooms.get(room, [])
        inRoom = False

        for u in users:
            if u['session'] == user['session']:
                u['session'] = user['session']
                inRoom = True
                break
        
        # not in user list
        if inRoom == False:
            users.append(user)
            self.playrooms[room] = users

        # leave room for invalid sid
        leave_room(room, self.clients.get(user['session'], None))

        # save sid
        self.clients[user['session']] = request.sid
            
        # join room
        join_room(room)

        print str(users)
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
                if u['session'] == session:
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
        
                
        