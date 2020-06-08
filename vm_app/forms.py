''' Define forms for the application here. '''
from django.forms import ModelForm, Select, HiddenInput, Form, ChoiceField, DateTimeInput, widgets, Media
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Room, Coordinates, Activities, Profile
from tempus_dominus.widgets import DateTimePicker, DatePicker, TimePicker

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
    class Meta:
        model = Activities
        fields = '__all__'
        widgets = {
            'startdate' : DateTimePicker(),
            'enddate' : DateTimePicker()
        }

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
            'shape' : Select(attrs={"onChange" : 'myFunction(this);'}),
            'venue' : Select(attrs={"onChange" : 'changeImage(this)'})
        }

class CreateCoordinatesForm(ModelForm):
    ''' From for adding coordinates to room. with room as HiddenInput. '''
    class Meta:
        model = Coordinates
        fields = '__all__'
        widgets = {
            'room' : HiddenInput()
        }

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email'}