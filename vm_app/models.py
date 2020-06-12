''' Database models added here '''
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group, AbstractUser
from django.core.validators import validate_comma_separated_integer_list, MinLengthValidator, MaxLengthValidator

# Create your models here.

class HomeModuleNames(models.Model):
    ''' Model for module-names used on the front-page. '''
    name = models.CharField(max_length=20)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)

class HomeModules(models.Model):
    '''
    Model containing all possible homeModules.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

#CustomUser(AbstractUser):
#    ''' Custom User class implementing custom permissions. '''
#    pass
#    # add additional fields here
#    canViewVenues = models.ManyToManyField(Venue)
#
#    def __str__(self):
#        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    venues = models.ManyToManyField(Venue)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)

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
