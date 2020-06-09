from vm_app.models import Venue, Profile

def venues(request):
    user = request.user
    if user.is_authenticated:
        venue = request.user.profile.venues.all()
        return {'sidebar_venues' : venue}
    return {'sidebar_venues' : ()}