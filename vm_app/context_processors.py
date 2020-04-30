from vm_app.models import Venue

def venues(request):
    user = request.user
    venue = Venue.objects.filter(customuser=user)[:3]

    return {'sidebar_venues' : venue }