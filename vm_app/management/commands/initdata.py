from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
from vm_app.models import Profile
# from yourapp.models import User # if you have a custom user

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','initial_data.json')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        profile = Profile.objects.get(user=10)
        profile.venues.set([1])
        profile.save()