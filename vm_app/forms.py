''' Define forms for the application here. '''
from django.forms import ModelForm, Form, widgets, Media, ValidationError
from django.forms import Select, HiddenInput, ChoiceField, BooleanField
from django.contrib.auth.models import User, Permission
from tempus_dominus.widgets import DateTimePicker, DatePicker, TimePicker
import pytz
from .models import Room, Activities, Profile, Venue, Client_user_permissions



# TODO: FIX THIS.....
class SplitDateTimeWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for day and month
        _widgets = (
            DatePicker(),
            TimePicker()
        )
        super(SplitDateTimeWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time()]
        return [None, None]

    def _media(self):
        print(Media(DatePicker.media))
        return DatePicker.media

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        rendered_widgets.insert(-1, '<br/>')
        return u''.join(rendered_widgets)

class ActivityForm(ModelForm):
    '''
    Form for creating activities.
    Timezone of start and end is set to the timezone of the venue-country.
    '''
    class Meta:
        model = Activities
        fields = '__all__'
        widgets = {
            'startdate' : DateTimePicker(),
            'enddate' : DateTimePicker()
        }

    def save(self, commit=True):
        temp = super(ActivityForm, self).save(commit=False)
        venue = Venue.objects.get(room=temp.room)
        tz_name = pytz.country_timezones[venue.country]

        naivestart = temp.startdate.replace(tzinfo=None)
        naiveend = temp.enddate.replace(tzinfo=None)

        temp.startdate = pytz.timezone(tz_name[0]).localize(naivestart)
        temp.enddate = pytz.timezone(tz_name[0]).localize(naiveend)

        if commit:
            temp.save()
        return temp



class HomeModelNamesForm(Form):
    ''' docstring '''
    module = ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        modules = kwargs.pop('modules')
        super(HomeModelNamesForm, self).__init__(*args, **kwargs)
        self.fields['module'].choices = modules

class CreateRoomForm(ModelForm):
    ''' Form for creating rooms. Implementing onChange listener on shape-input. '''
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'venue' : Select(attrs={"onChange" : 'changeImage(this)'}),
            'shape' : HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        shape = cleaned_data.get("shape")
        coords = cleaned_data.get("coordinates")
        print(type(coords))

        if shape == 'rect':
            coord_amount = 4

        if coord_amount != len(coords.split(',')):
            msg = ValidationError("Not the expected amount of coordinates.")
            self.add_error('coordinates', msg)

        return cleaned_data

class ProfileForm(ModelForm):
    '''
    Form for changing user-profile.
    Implements a phone-number field that expects country-code.
    '''

    class Meta:
        model = Profile
        fields = {'phone_number',}

class UserForm(ModelForm):
    '''
    Form for changing user fields.
    Implemented fields: username, first_name, last_name, email
    '''
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}

class EditUserVenueForm(Form):
    '''
    Form for changing what venues user has access to.
    Creates boolean field for each venue,
    and sets the initial state to indicate whether the user currently has access or not.

    Expects the following kwargs:
    'user': The user wich permissions to change.
    'client': The currently selected client
    'venues': The applicable venues.
    '''

    user = None
    venues = None

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        client = kwargs.pop('client')
        venues = kwargs.pop('venues')
        self.user = user
        self.venues = venues
        perms = Client_user_permissions.objects.get(user=user, client=client)

        super(EditUserVenueForm, self).__init__(*args, **kwargs)

        for venue in venues:
            venue_obj = Venue.objects.get(pk=venue)
            venue_id = 'venue_' + str(venue)
            self.fields[venue_id] = BooleanField(label="Can see " + venue_obj.name, required=False)
            self.fields[venue_id].initial = perms.venues.filter(pk=venue).exists()

    def save(self):
        '''
        Override of the save function.
        Updates the m2m relationship according to valid booleanfields.
        '''

        for venue in self.venues:
            key = 'venue_' + str(venue)
            if self.cleaned_data.get(key):
                self.user.profile.venues.add(Venue.objects.get(id=venue))
            else:
                self.user.profile.venues.remove(Venue.objects.get(id=venue))

class EditUserForm(Form):
    '''
    Form to edit user permissions.

    Expects the following kwargs:
    'user': The user to be affected.
    '''

    user = None
    venue_can_edit = BooleanField(label="Can edit venues:", required=False)
    venue_can_delete = BooleanField(label="Can delete venues:", required=False)
    room_can_add = BooleanField(label="Can add rooms:", required=False)
    room_can_edit = BooleanField(label="Can edit rooms:", required=False)
    room_can_delete = BooleanField(label="Can delete rooms:", required=False)

    perms = {
        'venue_can_edit' : 'vm_app.change_venue',
        'venue_can_delete' : 'vm_app.delete_venue',
        'room_can_add' : 'vm_app.add_room',
        'room_can_edit' : 'vm_app.change_room',
        'room_can_delete' : 'vm_app.delete_room',
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(EditUserForm, self).__init__(*args, **kwargs)

        self.user = user

        for key, value in self.perms.items():
            self.fields[key].initial = user.has_perm(value)



    def save(self):
        '''
        Overridden save function.
        Updates the user_permissions m2m relationship according to valid boleanfields.
        '''

        for key, value in self.perms.items():
            permission = Permission.objects.get(codename=value.split('.')[1])
            if self.cleaned_data.get(key):
                self.user.user_permissions.add(permission)
            else:
                self.user.user_permissions.remove(permission)
