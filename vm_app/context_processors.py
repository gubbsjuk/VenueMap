from vm_app.models import Venue, Profile, Client

def venues(request):
    user = request.user
    if user.is_authenticated:
        venue = request.user.profile.venues.all()
        return {'sidebar_venues' : venue}
    return {'sidebar_venues' : ()}

def clients_get(request):
    user = request.user
    if user.is_authenticated:
        clients = user.clients.all()
        return {'sidebar_clients' : clients}
    return {'sidebar_clients' : ()}
