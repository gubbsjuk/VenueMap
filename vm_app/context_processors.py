from vm_app.models import Venue, Profile, Client,Client_user_permissions

def venues(request):
    user = request.user
    if user.is_authenticated:
        try:
            perms = Client_user_permissions.objects.get(user=user, client=user.profile.selected_client)
            venue = perms.venues.all()
        except Client_user_permissions.DoesNotExist:
            venue = None
        return {'sidebar_venues' : venue}
    return {'sidebar_venues' : ()}

def clients_get(request):
    user = request.user
    if user.is_authenticated:
        clients = user.clients.all()
        return {'sidebar_clients' : clients}
    return {'sidebar_clients' : ()}
