''' Database models added here '''
from django.db import models
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.core.validators import validate_comma_separated_integer_list
from phonenumber_field.modelfields import PhoneNumberField
import pytz

# Create your models here.

class HomeModuleNames(models.Model):
    ''' Model for module-names used on the front-page. '''
    name = models.CharField(max_length=20)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)



class Client(models.Model):
    '''
    Model for the clients:
    Fields:
    name: Client-name (CharField)
    billing_address: clients billing-address (CharField)
    users: Users beloning to this client. (m2m-Field, related_name="clients")
    '''

    name = models.CharField(max_length=50)
    billing_address = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name="clients", blank=True)
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
    country = models.CharField(max_length=2, choices=pytz.country_names.items())
    arenalayout = models.FileField(upload_to='arenalayouts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Print name as string in choice fields.
    def __str__(self):
        return u'{0}'.format(self.name)

class Client_user_permissions(models.Model):
    '''
    Model containing client specific permissions.
    Fields:
    user: affected user (ForeignKey to User, related_name="client_user_perms")
    client: affected client (ForeignKey to Client)
    permissions: applied permissions (m2m-field to Django.contrib.auth.models.Permission)
    venues: Venues that are visible to the user. (m2m-field to vm_app.models.Venue)
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_user_perms")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)
    venues = models.ManyToManyField(Venue)

    def __str__(self):
        return u'{0}'.format(self.client) + ' | ' + u'{0}'.format(self.user)

class Profile(models.Model):
    '''
    Profile model associated with every user.
    Fields:
    user: OneToOneField(User)
    phone_number: Users phone-number. Expects country-code. (PhoneNumberField)
    selected_client: Field to indicate currently selected client. (ForeignKey(Client))
    module1-4: Frontpagemodules. (ForeignKey(HomeModuleNames))
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    selected_client = models.ForeignKey(Client, on_delete=models.SET, blank=True, null=True)
    module1 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module1', null=True)
    module2 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module2', null=True)
    module3 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module3', null=True)
    module4 = models.ForeignKey(HomeModuleNames, on_delete=models.DO_NOTHING, related_name='module4', null=True)

@receiver(pre_delete, sender=Client)
def reset_client(**kwargs):
    '''
    Signal to set profile.selected_client to first in query upon deletion of selected_client.
    '''

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
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='room')
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


#TODO: Does this need to save profile when created=False ?
@receiver(post_save, sender=User)
def update_user_profile(instance, created, **kwargs):
    '''
    Signal to create or update profile upon User creation or update.
    '''

    if created:
        Profile.objects.create(user=instance)
        try:
            client = instance.clients.all()[:1].get()
            instance.profile.selected_client = client
        except Client.DoesNotExist:
            pass
    instance.profile.save()

@receiver(m2m_changed, sender=Client.users.through)
def create_client_perms(**kwargs):
    '''
    Signal to add or remove Client specific permission object on change to the Client.users m2m field.
    '''

    client = kwargs.pop('instance')
    action = kwargs.pop('action')
    if action == 'post_remove':
        pk_set = kwargs.pop('pk_set')
        for user_pk in pk_set:
            user = User.objects.get(pk=user_pk)
            try:
                Client_user_permissions.objects.get(client=client, user=user).delete()
            except Client_user_permissions.DoesNotExist:
                pass
    if action == 'post_add':
        pk_set = kwargs.pop('pk_set')
        for user_pk in pk_set:
            user = User.objects.get(pk=user_pk)
            if not Client_user_permissions.objects.filter(client=client, user=user).exists():
                entry = Client_user_permissions(user=user, client=client)
                entry.save()
