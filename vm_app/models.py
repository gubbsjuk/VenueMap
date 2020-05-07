''' Database models added here '''
from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group, AbstractUser

# Create your models here.

class HomeModuleNames(models.Model):
    ''' Model for module-names used on the front-page. '''
    name = models.CharField(max_length=20)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)

class HomeModules(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module1 = models.ForeignKey(HomeModuleNames, on_delete=models.CASCADE, related_name='module1')
    module2 = models.ForeignKey(HomeModuleNames, on_delete=models.CASCADE, related_name='module2')
    module3 = models.ForeignKey(HomeModuleNames, on_delete=models.CASCADE, related_name='module3')
    module4 = models.ForeignKey(HomeModuleNames, on_delete=models.CASCADE, related_name='module4')


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

    def __str__(self):
        return self.name
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
