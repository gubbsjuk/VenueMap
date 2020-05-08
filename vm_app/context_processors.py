from vm_app.models import Venue

def venues(request):
    user = request.user
    if user.is_authenticated:
        venue = Venue.objects.filter(customuser=user)[:3]
        return {'sidebar_venues' : venue}
    return {'sidebar_venues' : ()}