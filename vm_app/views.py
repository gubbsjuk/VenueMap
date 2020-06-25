''' Define views attached to templates here. '''
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from .models import Venue, Room, Activities, HomeModuleNames, Profile, Client_user_permissions, Client
from .forms import CreateRoomForm, HomeModelNamesForm, ActivityForm, UserForm, ProfileForm, EditUserForm, EditUserVenueForm
from django.contrib.auth.models import User

# Create your views here.
def home_view(request):
    ''' base/start page view '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            #OPTIMIZE: Can this be deleted?
            homemodulenames = HomeModuleNames.objects.all().values_list('id', 'name')
            #
            modulenames = json.dumps(list(homemodulenames))
            homemoduleform = HomeModelNamesForm(modules=homemodulenames)
            context = {
                'homemodulenames' : modulenames,
                'homemoduleform' : homemoduleform
            }

            return render(request, 'home.html', context)

        #Return login form if not logged in.
        return HttpResponseRedirect(reverse('login'))

    #OPTIMIZE: IFs / Safe=False
    #Erstatt IF statements med noe annet?
    #Forsk på safe=False, hvorfor måtte jeg det? Kan jeg optimalisere for å få det bort?
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.POST.__contains__('modulePos'):
                modulepos = int(request.POST.__getitem__('modulePos'))
                modules = Profile.objects.get(user_id=request.user)
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
    '''
    Returns jsonobj. with the corresponding data according to the requested module.
    '''

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
            activities = filter_activities_by_user(request)
            if module.name == 'today':
                print("in today")
                activities = activities.filter(
                    startdate__gte=timezone.now().replace(hour=0, minute=0, second=0),
                    enddate__lte=timezone.now().replace(hour=23, minute=59, second=59))[:5]
                print(activities)
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
    '''
    Filter activities to activities in rooms the user has access to.
    '''

    rooms = filter_rooms_by_user(request)
    print(rooms)
    activities = Activities.objects.filter(room__in=rooms)

    return activities

def filter_venues_by_clients(request):
    ''' Utilitary function to filter Venues by their assigned client. '''
    current_clients = request.user.clients.all()
    return Venue.objects.filter(client__in=current_clients)

def filter_venues_by_user(request):
    ''' Utilitary function to filter Venues by user permitted to view.
        Currently not implemented and returns Venue.objects.get() '''
    venue = request.user.client_user_perms.venues.all()
    return venue

def filter_rooms_by_user(request):
    '''
    Filter rooms to rooms in venues the user has access to.
    '''

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
    context = {
        "venue" : venue,
        "rooms" : rooms,
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

@permission_required('vm_app.add_room')
def new_room_create_view(request):
    '''
    rewrite of room_create_view
    TODO: write better docstring and rename function
    '''
    if request.method == 'GET':
        # Get-request without a shape.
        room_form = CreateRoomForm()
        #coord_form = CreateCoordinatesForm()
        venues = filter_venues_by_user(request)
        room_form.fields['venue'].queryset = venues
        context = {
            'room_form' : room_form,
            'venues' : venues
        }
        return render(request, 'room/room_create.html', context)

    if request.method == 'POST':
        room_form = CreateRoomForm(request.POST)
        # TODO: Write custom validation of the formset
        # checking if formset is valid except reference to room PK
        # OPTIMALIZE: Using comma-separated with custom validation to check amount of numbers stops having to use AJAX and a for loop to iterate formset.
        print(room_form.errors)
        if room_form.is_valid():
            #savedmodel = room_form.save()
            #coord_form = CreateCoordinatesForm(request.POST)
            #coord_form.fields['room'].initial  = savedmodel.pk
            #if coord_form.is_valid():
                #form.save()
            return HttpResponseRedirect(reverse('room_manage_view'))

def room_manage_view(request):
    ''' View for managing rooms '''
    venues = filter_venues_by_user(request)
    print(venues)
    context = {
        'venues' : venues,
    }
    return render(request, 'room/room_manage.html', context)

def room_list_view(request):
    ''' View that lists rooms. Intended to be used with room_manage_view
        Filter can be set with GET.method where the data is the venue.PK'''
    venues = filter_venues_by_user(request)
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
    '''
    View of activitylist. returns populated activity_list.html.
    Requires kwargs "max" for max activites.
    '''
    maxact = kwargs.pop('max')
    rooms = filter_rooms_by_user(request)
    if maxact:
        activities = Activities.objects.filter(room__in=rooms)[:maxact]

    activities = Activities.objects.filter(room__in=rooms)
    context = {
        'activities' : activities
    }

    return render(request, 'activities_list.html', context)

def activity_create_view(request):
    '''
    View for creating new activities. Returns activity_create.html with a form named "form"
    '''

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        print(form.errors)
        if form.is_valid():
            savedmodel = form.save()
            return HttpResponse(savedmodel.pk)
    form = ActivityForm()
    return render(request, 'activity_create.html', {'form' : form})

def profile_update_view(request):

    #TODO: Filter out changed data and only update that.
    if request.method == "GET":
        initial_data_user = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        initial_data_profile = {
            'phone_number' : request.user.profile.phone_number,
        }
        
        user_form = UserForm(initial=initial_data_user)
        profile_form = ProfileForm(initial=initial_data_profile)

    if request.method == "POST":
        instance = request.user
        user_form = UserForm(request.POST, instance=instance)
        profile_form = ProfileForm(request.POST, instance=instance.profile)
        print(request.POST)
        if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            print(instance.profile)
            profile_form.save()

    context = {
        'userForm' : user_form,
        'profileForm' : profile_form
    }

    return render(request, 'profile_form.html', context)

@permission_required('auth.change_permission')
def manage_users_view(request):
    client = request.user.profile.selected_client
    users = User.objects.filter(clients=client)

    return render(request, 'user/manage_users.html', {'usrs' : users})

@permission_required('auth.change_permission')
def edit_user_view(request, pk):
    user = User.objects.get(pk=pk)
    client = request.user.profile.selected_client
    perms = Client_user_permissions.objects.get(user=request.user, client=client)
    venues = perms.venues.all().values_list('id', flat=True)
    rClients = request.user.clients.all().values_list('id', flat=True)

    if user.clients.filter(id__in=rClients).exists():
        if request.method == 'GET':
            form = EditUserForm(user=user)
            venue_form = EditUserVenueForm(user=user, venues=venues, client=client)
        if request.method == 'POST':
            form = EditUserForm(request.POST, user=user)
            venue_form = EditUserVenueForm(request.POST, user=user, venues=venues, client=client)
            if form.is_valid() and venue_form.is_valid():
                form.save()
                venue_form.save()
                return redirect('manage_users_view')

        context = {
            'user' : user,
            'form' : form,
            'venue_form' : venue_form
            }

        return render(request, 'user/edit_user.html', context)
    return HttpResponseForbidden()

def change_client(request, pk):
    user = request.user
    client_user_perms = Client_user_permissions.objects.get(client=pk, user=user)

    user.user_permissions.set(client_user_perms.permissions.all())
    user.profile.selected_client = Client.objects.get(pk=pk)
    user.save()

    return redirect(request.META['HTTP_REFERER'])