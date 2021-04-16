"""confyroom2000 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from conf_web.views import AddRooms, AllRooms, DelRoom, ModRoom, Reservation, RoomDetails, Search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-rooms', AddRooms.as_view()),
    path('all-rooms', AllRooms.as_view(), name="all-rooms"),
    path('room/delete/<int:room_id>', DelRoom.as_view()),
    path('room/modify/<int:room_id>', ModRoom.as_view()),
    path('room/reserve/<int:room_id>', Reservation.as_view()),
    path('room/details/<int:room_id>', RoomDetails.as_view()),
    path('search/', Search.as_view()),
]

urlpatterns += staticfiles_urlpatterns()