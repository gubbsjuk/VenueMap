''' Define views attached to templates here. '''
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.forms import formset_factory
from django.utils import timezone
from .models import Venue, Room, Coordinates, Activities, HomeModuleNames, HomeModules
from .forms import CreateRoomForm, CreateCoordinatesForm, HomeModelNamesForm


# Create your views here.
def home_view(request):
    ''' base/start page view '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            homemodulenames = HomeModuleNames.objects.all().values_list('id', 'name') # Can this be deleted?
            modulenames = json.dumps(list(homemodulenames))
            homemoduleform = HomeModelNamesForm(modules=homemodulenames)
            context = {
                'homemodulenames' : modulenames,
                'homemoduleform' : homemoduleform
            }

            return render(request, 'home.html', context)
        return render(request, 'home.html', {})
    
    #OPTIMIZE: IFs / Safe=False
    #Erstatt IF statements med noe annet?
    #Forsk på safe=False, hvorfor måtte jeg det? Kan jeg optimalisere for å få det bort?
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.__contains__('modulePos'):
                modulepos = int(request.POST.__getitem__('modulePos'))
                modules = HomeModules.objects.get(user_id=request.user)
                # TODO: Fill in rest of modulepositions
                # Better way to do this?
                if request.POST.__getitem__('update') == "true":
                    module_pk = int(request.POST.__getitem__('module'))
                    selectedmodule = HomeModuleNames.objects.get(pk=module_pk)
                    if modulepos == 1:
                        modules.module1 = selectedmodule
                    if modulepos == 2:
                        modules.module2 = selectedmodule
                    if modulepos == 3:
                        modules.module3 = selectedmodule
                    if modulepos == 4:
                        modules.module4 = selectedmodule
                    if modulepos == 5:
                        modules.module5 = selectedmodule
                    modules.save()
                    data = return_module(request, selectedmodule)
                elif request.POST.__getitem__('update') == "false":
                    if modulepos == 1:
                        data = return_module(request, modules.module1)
                    if modulepos == 2:
                        data = return_module(request, modules.module2)
                    if modulepos == 3:
                        data = return_module(request, modules.module3)
                    if modulepos == 4:
                        data = return_module(request, modules.module4)
                    if modulepos == 5:
                        data = return_module(request, modules.module5)
                return JsonResponse(data, safe=False)

def return_module(request, module):
    data = []
    header = {'header' : module.pk}
    data.append(header)

    if module.name:
        if module.name == 'venue':
            venues = filter_venues_by_user(request)
            for venue in venues:
                jsonobj = {'name' : venue.name,
                           'pk' : venue.pk}
                data.append(jsonobj)

        if module.name == 'today' or module.name == 'activities':
            print("in today or activities")
            activities = filter_activities_by_user(request)
            if module.name == 'today':
                activities = activities.filter(
                    startdate__gte=timezone.now().replace(hour=0, minute=0, second=0),
                    enddate__lte=timezone.now().replace(hour=23, minute=59, second=59))[:5]
            for act in activities:
                jsonobj = {
                    'name'   : act.name,
                    'start'  : act.startdate,
                    'end'    : act.enddate,
                    'room'   : act.room.name,
                    'pk'     : act.pk
                    }
                data.append(jsonobj)

        if module.name == 'rooms':
            rooms = filter_rooms_by_user(request)
            for room in rooms:
                jsonobj = {
                    'name' : room.name,
                    'roomtype' : room.roomtype.name,
                    'venue' : room.venue.name,
                    'pk' : room.pk
                }
                data.append(jsonobj)
        return data

def filter_activities_by_user(request):
    rooms = filter_rooms_by_user(request)
    print(rooms)
    activities = Activities.objects.filter(room__in=rooms)

    return activities

def filter_venues_by_usergroup(request):
    ''' Utilitary function to filter Venues by their assigned client. '''
    current_usergroups = request.user.groups.all()
    return Venue.objects.filter(client__in=current_usergroups)

def filter_venues_by_user(request):
    ''' Utilitary function to filter Venues by user permitted to view.
        Currently not implemented and returns Venue.objects.get() '''
    user = request.user
    venue = Venue.objects.filter(customuser=user)

    return venue

def filter_rooms_by_user(request):
    if not request.user.is_anonymous:
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

        if search_value:
            #TODO: IMPLEMENT MORE SHAPES HERE
            if search_value == 'rect':
                max_coords = 4

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
