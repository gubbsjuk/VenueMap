''' Define views attached to templates here. '''
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
from django.views import View
from .models import Venue, Room, Coordinates, Activities, HomeModuleNames, HomeModules
from .forms import CreateRoomForm, CreateCoordinatesForm

# Create your views here.
def home_view(request):
    ''' base/start page view '''

    if request.method == 'GET':
        if request.GET.__contains__('modulePos'):
            result = int(request.GET.__getitem__('modulePos'))
            modules = HomeModules.objects.get(user_id=request.user)
            print(result)
            print(modules.module1)
            if result == 1:
                print("in result == 1")
                data = return_module(request, str(modules.module1))
                return JsonResponse(data, safe=False)
            if result == 'venue':
                venues_view(request)
            if result == 'today':
                activities_view(request, max=10)
        
        homemodulenames = HomeModuleNames.objects.all()
        context = {
            'homemodulenames' : homemodulenames
        }

    return render(request, 'home.html', context)

def return_module(request, module):
    print("in return function")
    if module == 'venue':
        print("module is venue!")
        venues = filter_venues_by_user(request)
        data = []
        d = {'header' : module}
        data.append(d)
        for venue in venues:
            jsonobj = {'name' : venue.name, 
                        'pk' : venue.pk}
            data.append(jsonobj)
        
        return data


def filter_venues_by_usergroup(request):
    ''' Utilitary function to filter Venues by their assigned client. '''
    current_usergroups = request.user.groups.all()
    return Venue.objects.filter(client__in=current_usergroups)

def filter_venues_by_user(request):
    ''' Utilitart function to filter Venues by user permitted to view.
        Currently not implemented and returns Venue.objects.get() '''
    user = request.user
    venue = Venue.objects.filter(customuser=user)

    return venue

def filter_rooms_by_user(request):
    venues = filter_venues_by_user(request)
    rooms = Room.objects.filter(venue__in=venues)

    return rooms

def venues_view(request):
    ''' View that returns venues filtered by client.
        Context: 'venues' : venue '''
    venue = filter_venues_by_user(request)
    context = {
        "venues" : venue,
    }
    return render(request, 'venues.html', context)

def imgmap_view(request, pk):
    ''' Docstring, slutter du å mase nå? '''
    venue = Venue.objects.get(pk=pk)
    rooms = Room.objects.filter(venue=venue)
    coordmap = Coordinates.objects.filter(room__in=rooms)
    context = {
        "venue" : venue,
        "rooms" : rooms,
        "coordmap" : coordmap,
    }

    return render(request, 'imgmap_viewer.html', context)

def room_detail(request):
    ''' Docstring, slutter du å mase nå? '''
    search_value = request.GET.get("room", None)

    if search_value:
        room = Room.objects.get(pk=int(search_value))
        activities = Activities.objects.filter(room=room)

        context = {
            "room" : room,
            "activities" : activities,
        }

        return render(request, 'room_detail.html', context)

    return render(request, 'room_detail.html', {})

def room_create_view(request):
    ''' View for creating a new room.
        Valid post method returns HttpResponse with primary-key of the room '''

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.errors)
            savedmodel = form.save()
            return HttpResponse(savedmodel.pk)

        context = {
            'form' : form
        }
        return render(request, 'room/room_create.html', context)

    #if not POST, create the form. Filter venues by venues belonging to the client.
    form = CreateRoomForm()
    form.fields['venue'].queryset = filter_venues_by_usergroup(request)
    context = {
        'form' : form,
    }
    return render(request, 'room/room_create.html', context)

def room_create_coordinates_view(request):
    ''' View for creating coordinates belonging to a room.
        Intended to be used with "room_create_view.
        Awaits a GET-method requesting the expected amount of coordinate-forms to define the shape.
        '''
    max_coords = 0
    if request.method == 'GET':
        search_value = request.GET.get("shape", None)

        print("Search value:" + search_value)
        if search_value:
            ##IMPLEMENT MORE SHAPES HERE
            if search_value == 'rect':
                max_coords = 4
                print("Setting maxforms to: " + str(max_coords))

            CoordinatesFormSet = formset_factory(CreateCoordinatesForm, extra=max_coords)
            formset = CoordinatesFormSet()
            context = {
                'formset' : formset,
            }
            return render(request, 'room/room_create_coordinates.html', context)

    if request.method == 'POST':
        CoordinatesFormSet = formset_factory(CreateCoordinatesForm, extra=max_coords)
        formset = CoordinatesFormSet(request.POST)
        print(formset.errors)
        if formset.is_valid():
            for form in formset:
                form.save()

            return HttpResponseRedirect(reverse('room_manage'))

def room_manage_view(request):
    ''' View for managing rooms '''
    venues = filter_venues_by_usergroup(request)

    context = {
        'venues' : venues,
    }
    return render(request, 'room/room_manage.html', context)

def room_list_view(request):
    ''' View that lists rooms. Intended to be used with room_manage_view
        Filter can be set with GET.method where the data is the venue.PK'''
    venues = filter_venues_by_usergroup(request)
    #Result is not 'noFilter' or GET doesnt contain key define rooms to:
    rooms = Room.objects.filter(venue__in=venues)
    if request.method == 'GET':
        if request.GET.__contains__('venuePK'):
            result = request.GET.__getitem__('venuePK')
            if result != 'noFilter':
                #Result has a a value and its not noFilter. define rooms to:
                rooms = Room.objects.filter(venue=result)

        context = {
            'rooms' : rooms,
            'venues' : venues,
        }
        return render(request, 'room/room_list.html', context)

def activities_view(request, **kwargs):
    maxact = kwargs.pop('max')
    rooms = filter_rooms_by_user(request)
    if maxact:
        activities = Activities.objects.filter(room__in=rooms)[:maxact]

    activities = Activities.objects.filter(room__in=rooms)
    context = {
        'activities' : activities
    }

    return render(request, 'activities_list.html', context)