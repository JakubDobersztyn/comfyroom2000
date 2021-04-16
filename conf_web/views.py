from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from conf_web.models import Rooms


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

        return render(request, template_name="main.html", context={'middle': 'reservation.html'})