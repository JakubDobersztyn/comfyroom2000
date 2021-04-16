import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from conf_web.models import Rooms, RoomReservations


class AddRooms(View):
    def get(self, request):
        return render(request, template_name="main.html", context={'middle': 'AddRooms.html'})

    def post(self, request):
        room_name = request.POST.get('room_name')
        room_cap = request.POST.get('room_cap')
        projector = request.POST.get('projector')
        if not room_name:
            return render(request, template_name='main.html',
                          context={'middle': 'AddRooms.html', 'error': "Nie podano nazwy sali"})
        if int(room_cap) <= 0:
            return render(request, template_name='main.html',
                          context={'middle': 'AddRooms.html', 'error': "Pojemność sali nie może być mniejsza od 1"})
        if Rooms.objects.filter(room_name=room_name).first():
            return render(request, template_name='main.html',
                          context={'middle': 'AddRooms.html', 'error': "Sala o tej nazwie już istnieje"})
        room_cap = int(room_cap)
        projector = bool(projector)
        Rooms.objects.create(room_name=room_name, room_cap=room_cap, projector=projector)
        info = f"Dodano sale '{room_name}'"
        return render(request, template_name='main.html',
                      context={'middle': 'AddRooms.html', 'error': info})


class AllRooms(View):
    def get(self, request):
        rooms = Rooms.objects.order_by('id')
        if rooms:
            for room in rooms:
                reservation_dates = [reservation.date for reservation in room.roomreservations_set.all()]
                room.reserved = datetime.date.today() in reservation_dates
            return render(request, template_name='main.html', context={"middle": "allrooms.html", "rooms": rooms})

        return render(request, template_name='main.html',
                      context={'middle': "norooms.html"})


class DelRoom(View):
    def get(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except:
            return render(request, template_name='main.html',
                          context={'middle': 'info.html', 'info': 'Brak sali o tym id'})
        room.delete()
        return redirect("all-rooms")


class ModRoom(View):
    def get(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except:
            return render(request, template_name='main.html',
                          context={'middle': 'info.html', 'info': 'Brak sali o tym id'})

        return render(request, template_name="main.html", context={'middle': 'modifyroom.html', 'room': room})

    def post(self, request, room_id):
        # room_id = request.POST.get('room_id')
        room_name = request.POST.get('room_name')
        room_cap = request.POST.get('room_cap')
        projector = request.POST.get('projector')
        if not room_name:
            return render(request, template_name='main.html',
                          context={'middle': 'modifyroom.html', 'error': "Nie podano nazwy sali"})
        if int(room_cap) <= 0:
            return render(request, template_name='main.html',
                          context={'middle': 'modifyroom.html', 'error': "Pojemność sali nie może być mniejsza od 1"})

        room = Rooms.objects.get(id=room_id)
        if room_name != room.room_name:
            if Rooms.objects.filter(room_name=room_name).first():
                return render(request, template_name='main.html',
                              context={'middle': 'modifyroom.html', 'error': "Sala o tej nazwie już istnieje",
                                       'room': room})

        room_cap = int(room_cap)
        projector = bool(projector)
        room.room_name = room_name
        room.room_cap = room_cap
        room.projector = projector
        room.save()
        info = f"zmieniono sale '{room_name}'"
        rooms = Rooms.objects.order_by('id')
        return render(request, template_name='main.html',
                      context={'middle': 'allrooms.html', 'info': info, 'rooms': rooms})


class Reservation(View):
    def get(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except:
            return render(request, template_name='main.html',
                          context={'middle': 'info.html', 'info': 'Brak sali o tym id'})
        reservations = room.roomreservations_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, template_name="main.html", context={'middle': 'reservation.html', 'reservations': reservations})


    def post(self, request, room_id):
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        try:
            room = Rooms.objects.get(id=room_id)
        except:
            return render(request, template_name='main.html',
                          context={'middle': 'info.html', 'info': 'Brak sali o tym id'})
        reservations = room.roomreservations_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        if not date:
            return render(request, template_name="main.html",
                          context={'middle': 'reservation.html', 'reservations': reservations, 'error': 'Wybierz datę'})
        if date < str(datetime.date.today()):
            return render(request, template_name="main.html",
                          context={'middle': 'reservation.html', 'reservations': reservations, 'error': 'Data nie może być z przeszłości'})
        if RoomReservations.objects.filter(room=room, date=date):
            return render(request, template_name="main.html",
                          context={'middle': 'reservation.html', 'reservations': reservations, 'error': 'Sala tego dnia jest zajęta'})
        RoomReservations.objects.create(room=room, date=date,comment=comment)

        return redirect("all-rooms")


class RoomDetails(View):
    def get(self, request, room_id):
        try:
            room = Rooms.objects.get(id=room_id)
        except:
            return render(request, template_name='main.html',
                          context={'middle': 'info.html', 'info': 'Brak sali o tym id'})
        reservations = room.roomreservations_set.filter(date__gte=str(datetime.date.today()))
        return render(request, template_name="main.html",
                          context={'middle': 'roomdetails.html', 'room': room, 'reservations': reservations})

class Search(View):
    def get(self, request):
        room_name = request.GET.get('room_name')
        room_cap = request.GET.get('room_cap')
        room_cap = int(room_cap) if room_cap else 0
        projector = request.GET.get('projector') == "on"

        rooms = Rooms.objects.all()
        if projector:
            rooms = rooms.filter(projector=projector)
        if room_cap:
            rooms = rooms.filter(room_cap__gte=room_cap)
        if room_name:
            rooms = rooms.filter(room_name__contains=room_name)
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservations_set.all()]
            room.reserved = datetime.date.today() in reservation_dates

        return render(request, template_name='main.html', context={'middle': 'searchresults.html', 'rooms': rooms})
