from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
from vm_app.models import Profile, Client_user_permissions
# from yourapp.models import User # if you have a custom user

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_clients.json')
        call_command('loaddata', 'initial_users.json')
        call_command('loaddata', 'initial_venues.json')
        call_command('loaddata', 'initial_misc.json')
        call_command('loaddata', 'Home_modules.json')
        call_command('createsuperuser')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        
        perms_alesund = Client_user_permissions.objects.all().filter(user=10, client=1).get()
        perms_molde = Client_user_permissions.objects.all().filter(user=10, client=2).get()
        perms_ulstein = Client_user_permissions.objects.all().filter(user=10, client=3).get()
        
        perms_alesund.venues.set([1,2])
        perms_molde.venues.set([3])
        perms_ulstein.venues.set([4])
 
