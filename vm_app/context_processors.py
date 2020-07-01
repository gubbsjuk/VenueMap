from vm_app.models import Client_user_permissions

def venues(request):
    '''
    context_processor to make available venues visble
    via 'sidebar_venues' tag if the user is authenticated
    '''

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
    '''
    context_processor to make available clients visble
    via 'sidebar_clients' tag if the user is authenticated
    '''

    user = request.user
    if user.is_authenticated:
        clients = user.clients.all()
        return {'sidebar_clients' : clients}
    return {'sidebar_clients' : ()}
