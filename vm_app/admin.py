''' Admin module features added here.. '''
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin
from .models                    import Venue, Room, RoomType, Shape, Coordinates, Activities, HomeModuleNames, HomeModules, Profile

class VenueAdmin(admin.ModelAdmin):
    ''' Admin module for Venue model '''
    pass

class RoomAdmin(admin.ModelAdmin):
    ''' Admin module for Room model '''
    pass

class RoomTypeAdmin(admin.ModelAdmin):
    ''' Admin module for RoomType model '''
    pass

class ShapeAdmin(admin.ModelAdmin):
    ''' Admin module for Shape model '''
    pass

class CoordinatesAdmin(admin.ModelAdmin):
    ''' Admin module for Coordinates model '''
    pass

class ActivityAdmin(admin.ModelAdmin):
    ''' Admin module for Activity model '''
    pass

class HomeModuleNamesAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

class ProfileAdmin(admin.ModelAdmin):
    ''' Admin module for Profile model '''
    filter_horizontal = ('venues',)

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Shape, ShapeAdmin)
admin.site.register(Coordinates, CoordinatesAdmin)
admin.site.register(Activities, ActivityAdmin)
admin.site.register(HomeModuleNames, HomeModuleNamesAdmin)
admin.site.register(HomeModules)
