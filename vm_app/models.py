''' Database models added here '''
from django.db import models
from django.contrib.auth.models import Group, AbstractUser

# Create your models here.

class Venue(models.Model):
    ''' Model for venues '''
    name = models.CharField(max_length=20)
    webpage = models.URLField()
    streetaddress = models.CharField(max_length=100)
    zipcode = models.SmallIntegerField()
    city = models.CharField(max_length=100)
    arenalayout = models.FileField(upload_to='arenalayouts')
    client = models.ForeignKey(Group, on_delete=models.CASCADE)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)

class CustomUser(AbstractUser):
    ''' Custom User class implementing custom permissions. '''
    pass
    # add additional fields here
    canViewVenues = models.ManyToManyField(Venue)


    def __str__(self):
        return self.username

class RoomType(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    name = models.CharField(max_length=20,)


    def __str__(self):
        return u'{0}'.format(self.name)

class Room(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    name = models.CharField(max_length=20)
    roomtype = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    shape = models.ForeignKey('Shape', on_delete=models.CASCADE)


class Shape(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    shape = models.CharField(max_length=10)


    def __str__(self):
        return u'{0}'.format(self.shape)

class Coordinates(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    coordinate = models.SmallIntegerField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)


class Activities(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    name = models.CharField(max_length=100)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
