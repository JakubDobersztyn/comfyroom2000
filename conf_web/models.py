from django.db import models


# Create your models here.

class Rooms(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_cap = models.IntegerField()
    projector = models.BooleanField(default=False)


class RoomReservations(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room', 'date',)
