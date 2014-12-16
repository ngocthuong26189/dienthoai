#!/usr/bin/env python
# -*- coding: utf-8 -*-

from autobahn.twisted.websocket import WebSocketServerProtocol,WebSocketServerFactory
from uuid import uuid1
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

employees = []
users = []
cid = 0

def emp():
    pos = 0
    while True:
        pos = pos + 1
        if pos >= len(employees):
            pos = 0
        yield employees[pos]

emp_assign = emp()

class MyServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        token_array = request.params.get('token', None)
        self.cid = str(uuid1())
        print self.cid
        users.append(self)
        if token_array:
            # should implement employe authentication here
            self.token = token_array[0]
            employees.append(self)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):

        def close_partner(cids, seq):
            clients = filter(lambda item: item.cid in cids, seq)
            for c in clients:
                c.sendClose()

        def send_msg(cid, msg):
            clients = filter(lambda item: item.cid == cid, users)
            for c in clients:
                c.sendMessage(msg, False)
        # Set cid for this client when reconnect

        data = json.loads(payload.decode('utf-8'))
        if data['type'] == 'message':
            print data
            message = json.dumps({"type": "message", "from": self.cid, "content": str(data["content"])})
            send_msg(data['to'], message)
        elif data['type'] == 'reconnect':
            self.cid = data['content']
        elif data['type'] == 'close':
            self.sendClose()
            cids = data.get('cids')
            if cids:
                close_partner(cids, users)
                close_partner(cids, employees)
        elif data['type'] == 'connect':
            employe = emp_assign.next();
            emp_id = employe.cid
            msg = json.dumps({"type": "connect", "employe_id": emp_id})
            send_msg(emp_id, json.dumps({"type": "connect", "cid": self.cid}))
            self.sendMessage(msg)
        elif data['type'] == "reqcid":
            msg = json.dumps({"type": "respcid", "cid": self.cid})
            self.sendMessage(msg)

    def onClose(self, wasClean, code, reason):
        if self in users:
            users.remove(self)
        if self in employees:
            employees.remove(self)

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()
