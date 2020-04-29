''' Define forms for the application here. '''
from django.forms import ModelForm, Select, HiddenInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Room, Coordinates, CustomUser

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
