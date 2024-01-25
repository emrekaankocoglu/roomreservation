from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .interface import TCPInterfaceInstance
from .forms import RoomForm, EventForm, ReserveForm, QueryForm, ViewForm
from tcp.packet import Packet
import os
from django.contrib.auth.decorators import login_required

TOKEN = os.environ.get("TOKEN")

# Create your views here.

class Login(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('roomreservation:listobject') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

@login_required(login_url='/login/')
def listobject(request):
    with TCPInterfaceInstance() as tcp_interface:
        user = request.user.username
        tcp_interface.send(Packet("REQUEST", {"command":"listObject"}, {"username":user, "token":TOKEN}))
        packet = tcp_interface.receive()
        if packet.message == "ERROR":
            return render(request, "error.html", {"error":packet.data['response']})
        return render(request, "listobject.html", {"objects":packet.data['response']})

@login_required(login_url='/login/')
def getid(request, object_id):
    with TCPInterfaceInstance() as tcp_interface:
        tcp_interface.send(Packet("REQUEST", {"command":"getid", "id":object_id}, {"username":"emre", "token":TOKEN}))
        packet = tcp_interface.receive()
        if packet.message == "ERROR":
            return render(request, "error.html", {"error":packet.data['response']})
        return render(request, "getid.html", {"object":packet.data['response']})

@login_required(login_url='/login/')
def listRoom(request, organization_id):
    with TCPInterfaceInstance() as tcp_interface:
        user = request.user.username
        tcp_interface.send(Packet("REQUEST", {"command": "listRoom", "organization": organization_id}, {"username": user, "token":TOKEN}  ))
        packet = tcp_interface.receive()
        if packet.message == "ERROR":
            return render(request, "error.html", {"error": packet.data['response']})
        rooms = [v.getdict() for k,v in packet.data['response'].items()]
        for room in rooms:
            room["workinghours"] = (room["workinghours"][0].strftime("%H:%M"), room["workinghours"][1].strftime("%H:%M"))

        return render(request, "listroom.html", {"rooms": rooms, "organization_id":organization_id})

@login_required(login_url='/login/')   
def createRoom(request, organization_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                user = request.user.username
                tcp_interface.send(Packet("REQUEST", {"command": "createRoom", "organization": organization_id, "room": form.cleaned_data}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return redirect("roomreservation:listroom", organization_id=organization_id)
        else:
            form = RoomForm()
        return render(request, "createroom.html", {"form": form, "organization_id":organization_id})
    
@login_required(login_url='/login/')
def updateRoom(request, organization_id, room_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                user = request.user.username
                room = {"id": room_id, "name": form.cleaned_data["name"], "x": form.cleaned_data["x"], "y": form.cleaned_data["y"], "capacity": form.cleaned_data["capacity"], "workinghours": form.cleaned_data["workinghours"], "permissions": form.cleaned_data["permissions"]}
                tcp_interface.send(Packet("REQUEST", {"command": "updateRoom", "organization": organization_id, "room": room, "id": room_id}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return redirect("roomreservation:listroom", organization_id=organization_id)
        else:
            tcp_interface.send(Packet("REQUEST", {"command": "listRoom", "organization": organization_id}, {"username": request.user.username, "token": TOKEN}))
            packet = tcp_interface.receive()
            if packet.message == "ERROR":
                return render(request, "error.html", {"error": packet.data['response']})
            room = packet.data['response'][room_id].getdict()
            room["workinghours_start"] = room["workinghours"][0].strftime("%H:%M")
            room["workinghours_end"] = room["workinghours"][1].strftime("%H:%M")
            form = RoomForm(initial=room)
        return render(request, "updateroom.html", {"form": form, "organization_id":organization_id, "room_id":room_id})
    
@login_required(login_url='/login/')
def deleteRoom(request, organization_id, room_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            user = request.user.username
            tcp_interface.send(Packet("REQUEST", {"command": "deleteRoom", "organization": organization_id, "room": {"id": room_id}}, {"username": user, "token": TOKEN}))
            packet = tcp_interface.receive()
            if packet.message == "ERROR":
                return render(request, "error.html", {"error": packet.data['response']})
            return redirect("roomreservation:listroom", organization_id=organization_id)
        else:
            return render(request, "deleteroom.html", {"organization_id":organization_id, "room_id":room_id})
    

@login_required(login_url='/login/')
def createEvent(request, organization_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                user = request.user.username
                tcp_interface.send(Packet("REQUEST", {"command": "createEvent", "organization": organization_id, "event": form.cleaned_data}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return redirect("roomreservation:listevent", organization_id=organization_id)
        else:
            form = EventForm()
        return render(request, "createevent.html", {"form": form, "organization_id":organization_id})
    


@login_required(login_url='/login/')
def updateEvent(request, organization_id, event_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                user = request.user.username
                event = {"id": event_id, "title": form.cleaned_data["title"], "description": form.cleaned_data["description"], "category": form.cleaned_data["category"], "capacity":form.cleaned_data["capacity"], "duration":form.cleaned_data["duration"], "weekly": form.cleaned_data["weekly"], "permissions": form.cleaned_data["permissions"]}
                tcp_interface.send(Packet("REQUEST", {"command": "updateEvent", "organization": organization_id, "event": event}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return redirect("roomreservation:listevent", organization_id=organization_id)
        else:
            tcp_interface.send(Packet("REQUEST", {"command": "listEvent", "organization": organization_id}, {"username": request.user.username, "token": TOKEN}))
            packet = tcp_interface.receive()
            if packet.message == "ERROR":
                return render(request, "error.html", {"error": packet.data['response']})
            event = packet.data['response'][event_id].getdict()
            if event.get("weekly"):
                event["weekly"] = event["weekly"].strftime("%Y-%m-%dT%H:%M")
            form = EventForm(initial=event)
        return render(request, "updateevent.html", {"form": form, "organization_id":organization_id, "event_id":event_id})
    
@login_required(login_url='/login/')
def deleteEvent(request, organization_id, event_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            user = request.user.username
            tcp_interface.send(Packet("REQUEST", {"command": "deleteEvent", "organization": organization_id, "event": {"id": event_id}}, {"username": user, "token": TOKEN}))
            packet = tcp_interface.receive()
            if packet.message == "ERROR":
                return render(request, "error.html", {"error": packet.data['response']})
            return redirect("roomreservation:listevent", organization_id=organization_id)
        else:
            return render(request, "deleteevent.html", {"organization_id":organization_id, "event_id":event_id})
        


@login_required(login_url='/login/')   
def reserve(request,organization_id):
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = ReserveForm(request.POST)
            if form.is_valid():
                user = request.user.username
                tcp_interface.send(Packet("REQUEST", {"command": "reserve", "organization": organization_id, "event": {"id": form.cleaned_data["event"]}, "room": {"id":form.cleaned_data["room"]}, "start": form.cleaned_data["start"]}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return redirect("roomreservation:listevent", organization_id=organization_id)
        else:
            form = ReserveForm()
        return render(request, "reserve.html", {"form":form,"organization_id":organization_id})

@login_required(login_url='/login/')   
def addQuery(request, organization_id):
    user = request.user.username
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = QueryForm(request.POST)
            if form.is_valid():
                tcp_interface.send(Packet("REQUEST", {"command": "addQuery", "organization": organization_id, "query": form.cleaned_data}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                return render(request, "success.html", {"message": packet.data['response']})
        else:
            form = QueryForm()
        return render(request, "addquery.html", {"form":form,"organization_id":organization_id, "user": user})

@login_required(login_url='/login/')    
def listQuery(request, organization_id):
    user = request.user.username
    with TCPInterfaceInstance() as tcp_interface:
        tcp_interface.send(Packet("REQUEST", {"command": "listQuery"}, {"username": user, "token": TOKEN}))
        packet = tcp_interface.receive()
        if packet.message == "ERROR":
            return render(request, "error.html", {"error": packet.data['response']})
        queries = [v[0] if v[1] == organization_id else None for k,v in packet.data['response'].items()]
        return render(request, "listquery.html", {"queries": queries, "user": user})

@login_required(login_url='/login/')    
def roomView(request, organization_id):
    user = request.user.username
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = ViewForm(request.POST)
            if form.is_valid():
                tcp_interface.send(Packet("REQUEST", {"command": "roomView", "start": form.cleaned_data["start"], "end": form.cleaned_data["end"]}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                view = {k:[x[0].getdict() for x in v] for k,v in packet.data['response'].items()}
                return render(request, "roomview.html", {"view": view, "user": user})
        else:
            form = ViewForm()
        return render(request, "roomview.html", {"form":form,"organization_id":organization_id, "user": user, "token": TOKEN })

@login_required(login_url='/login/')
def dayView(request, organization_id):
    user = request.user.username
    with TCPInterfaceInstance() as tcp_interface:
        if request.method == 'POST':
            form = ViewForm(request.POST)
            if form.is_valid():
                tcp_interface.send(Packet("REQUEST", {"command": "dayView", "start": form.cleaned_data["start"], "end": form.cleaned_data["end"]}, {"username": user, "token": TOKEN}))
                packet = tcp_interface.receive()
                if packet.message == "ERROR":
                    return render(request, "error.html", {"error": packet.data['response']})
                view = {k:[{"event":x[0].getdict(), "room":x[1].getdict()} for x in v] for k,v in packet.data['response'].items()}
                print(view)
                return render(request, "dayview.html", {"view": view, "user": user})
        else:
            form = ViewForm()
        return render(request, "dayview.html", {"form":form,"organization_id":organization_id, "user": user, "token": TOKEN})

@login_required(login_url='/login/')
def listEvent(request, organization_id):
    with TCPInterfaceInstance() as tcp_interface:
        user = request.user.username
        tcp_interface.send(Packet("REQUEST",{"command": "listEvent", "organization": organization_id}, {"username": user, "token": TOKEN}))
        packet = tcp_interface.receive()
        if packet.message == "ERROR":
            return render(request, "error.html", {"error": packet.data['response']})
        events = [v.getdict() for k,v in packet.data['response'].items()]
        for event in events:
            if event.get("start"):
                event["start"] = event["start"].strftime("%Y-%m-%dT%H:%M")
            if event.get("weekly"):
                event["weekly"] = event["weekly"].strftime("%Y-%m-%dT%H:%M")
        return render(request, "listevent.html", {"events": events, "organization_id":organization_id})


