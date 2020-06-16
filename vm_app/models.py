''' Database models added here '''
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, Permission
from django.core.validators import validate_comma_separated_integer_list, MinLengthValidator, MaxLengthValidator

# Create your models here.

class HomeModuleNames(models.Model):
    ''' Model for module-names used on the front-page. '''
    name = models.CharField(max_length=20)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)



class Client(models.Model):
    name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name="clients")
    # TODO: Add more client specific information.
    
    def __str__(self):
        return u'{0}'.format(self.name)

class Venue(models.Model):
    ''' Model for venues '''
    name = models.CharField(max_length=20)
    webpage = models.URLField()
    streetaddress = models.CharField(max_length=100)
    zipcode = models.SmallIntegerField()
    city = models.CharField(max_length=100)
    arenalayout = models.FileField(upload_to='arenalayouts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)

class Client_user_permissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_user_perms")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return u'{0}'.format(self.client) + ' | ' + u'{0}'.format(self.user)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    venues = models.ManyToManyField(Venue)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    selected_client = models.ForeignKey(Client, on_delete=models.SET, blank=True, null=True)
    module1 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module1', null=True)
    module2 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module2', null=True)
    module3 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module3', null=True)
    module4 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module4', null=True)

@receiver(pre_delete, sender=Client)
def reset_client(sender, **kwargs):
    client = kwargs['instance']
    for profile in Profile.filter(selected_client=client):
        profile.selected_client = Client.users.filter(profile=profile).first()
        profile.save()

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
    shape = models.CharField(max_length=10, null=True, blank=True, default="")
    coordinates = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, blank=True, null=True, default="")

    def __str__(self):
        return self.name

class Activities(models.Model):
    ''' Docstring, slutter du å mase nå? '''
    name = models.CharField(max_length=100)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
