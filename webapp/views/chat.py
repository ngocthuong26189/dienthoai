import os
from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from models.user import User
import uuid
from services import system


customers = []
employees = []

class CustomerChat(BaseNamespace, RoomsMixin, BroadcastMixin):
    def initialize(self):
        customers.append(self)

    def on_message(self, data):
        employeeId = data.get('employeeId')
        room = data.get('room')
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        if name is None or email is None or message is None:
            return self.emit('error',{message:'must input your name, email and message'})
        emit_data = {'name':name,'email':email,'message':message,'type':'customer'}
        if employeeId is None:
            employee = get_employee(employees)
            if employee:
                self.emit("error","test....")
                customer_gen_room(self, employee,emit_data)
            else:
                return self.emit('error',{'message':'we are offline now'})
        else:
            employee = find_employee_by_id(employeeId, employees)
            if employee:
                if room:
                    if get_room_employee(room, emloyee):
                        self.emit_to_room(room, 'message',{'name':name,'email':email,'message':message,'type':'customer'})
                    else:
                        customer_gen_room(self, employee, emit_data)
                else:
                    customer_gen_room(self, employee, emit_data)
            else:
                return self.emit('error',{'message':'employee disconnected'})
   
    def recv_disconnect(self,*args, **kwargs):
        for room in self.session['rooms'].copy():
            self.emit_to_room(room,'customer_disconnected',{'customer':self.session.get('user')})
            # self.leave(room)
        if self in customers:
            customers.remove(self)
        super(CustomerChat, self).disconnect(*args, **kwargs)

class EmployeeChat(BaseNamespace, RoomsMixin, BroadcastMixin):
    def initialize(self):
        employees.append(self)
    
    def on_message(self, message):
        print message.get('data')

    def on_login(self,data):
        userId = data.get('userId')
        sid = data.get('sid')
        self.session['user'] = login(userId=userId, sid=sid)

    def recv_disconnect(self,*args, **kwargs):
        if self.session.get('user'):
            for room in self.session['rooms'].copy():
                self.emit_to_room(room,'employee_disconnected',{'employee':self.session.get('user')})
                # self.leave(room)
        print "nhan vien roi phong"
        if self in employees:
            employees.remove(self)
        super(EmployeeChat, self).disconnect(*args, **kwargs)

def login(userId=None, sid=None):
    if userId:
        user = User.objects(id=userId).get()
        if user.sid == sid:
            user.password = ''
            return user
    return None

def find_employee_by_id(id, employees):
    employee = None
    for employee in employees:
        if employee.session.get('user'):
            if employee.session.get('user').id == id:
                return employee
    return employee

def get_employee(employees):
    if len(employees) == 0:
        return None
    min = employees.pop()
    for employee in employees:
        if len(employee.session['rooms']) < len(min.session['rooms']):
            min = employee
    return min

def get_room_employee(room,emloyee):
    if emloyee.session.get('rooms'):
        for r in emloyee.session.get('rooms'):
            if r == room:
                return r
    return None

def customer_gen_room(customer, employee, emit_data):
    room = str(uuid.uuid4())
    emit_data['room'] = room
    customer.join(room)
    employee.join(room)
    customer.session['user'] = {'room':room,'name':emit_data.get('name'),'email':emit_data.get('email')}
    customer.emit('info',{'employeeId':str(employee.session['user'].id),'room':room})
    customer.emit_to_room(room, 'message',emit_data)

def chat(environ, start_response):
    if environ['PATH_INFO'].startswith('/socket.io'):
        return socketio_manage(environ, { '/customer': CustomerChat,'/employee':EmployeeChat })
    else:
        return start_response('404 NOT FOUND', [])

def run(host='' , port=8080):
    print "chat module run on port " + str(port)
    system.connect_mongo()
    SocketIOServer(('', port), chat, policy_server=False).serve_forever()
