from vm_app.models import Venue

def venues(request):
    current_usergroup = request.user.groups.all()[:1]
    venue = Venue.objects.filter(client=current_usergroup)[:3]

    return {'venues' : venue }