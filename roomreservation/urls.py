from django.urls import path
from . import views

app_name = "roomreservation"
urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('listobject/', views.listobject, name="listobject"),
    path('organizations/<int:organization_id>/listroom/', views.listRoom, name="listroom"),
    path('organizations/<int:organization_id>/createroom/', views.createRoom, name="createroom"),
    path('organizations/<int:organization_id>/updateroom/<int:room_id>/', views.updateRoom, name="updateroom"),
    path('organizations/<int:organization_id>/deleteroom/<int:room_id>/', views.deleteRoom, name="deleteroom"),
    path('organizations/<int:organization_id>/listevent/', views.listEvent, name="listevent"),
    path('organizations/<int:organization_id>/createevent/', views.createEvent, name="createevent"),
    path('organizations/<int:organization_id>/updateevent/<int:event_id>/', views.updateEvent, name="updateevent"),
    path('organizations/<int:organization_id>/deleteevent/<int:event_id>/', views.deleteEvent, name="deleteevent"),
    path('organizations/<int:organization_id>/reserve/', views.reserve, name="reserve"),
    path('organizations/<int:organization_id>/addquery/', views.addQuery, name="addquery"),
    path('organizations/<int:organization_id>/listquery/', views.listQuery, name="listquery"),
    path('organizations/<int:organization_id>/roomview/', views.roomView, name="roomview"),
    path('organizations/<int:organization_id>/dayview/', views.dayView, name="dayview"),
]