''' Define forms for the application here. '''
from django.forms import ModelForm, Select, HiddenInput, Form, ChoiceField, DateTimeInput, widgets, Media
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Room, Coordinates, CustomUser, Activities
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

class CustomUserCreationForm(UserCreationForm):
    ''' Custom form for creating users. Required when implementing CustomUser model '''

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    ''' Custom form for changeing users. Required when implementing CustomUser model '''

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CreateRoomForm(ModelForm):
    ''' Form for creating rooms. Implementing onChange listener on shape-input. '''
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'shape' : Select(attrs={"onChange" : 'myFunction(this);'})
        }

class CreateCoordinatesForm(ModelForm):
    ''' From for adding coordinates to room. with room as HiddenInput. '''
    class Meta:
        model = Coordinates
        fields = '__all__'
        widgets = {
            'room' : HiddenInput()
        }
