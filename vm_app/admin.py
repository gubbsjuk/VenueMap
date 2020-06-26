''' Admin module features added here.. '''
from django.contrib             import admin
from django.contrib.auth.admin  import UserAdmin
from .models                    import Venue, Room, RoomType, Activities, HomeModuleNames, Profile, Client, Client_user_permissions

class VenueAdmin(admin.ModelAdmin):
    ''' Admin module for Venue model '''
    pass

class RoomAdmin(admin.ModelAdmin):
    ''' Admin module for Room model '''
    pass

class RoomTypeAdmin(admin.ModelAdmin):
    ''' Admin module for RoomType model '''
    pass

class ActivityAdmin(admin.ModelAdmin):
    ''' Admin module for Activity model '''
    pass

class HomeModuleNamesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class Client_user_permissions_admin(admin.ModelAdmin):
    ''' Admin module for Profile model '''
    filter_horizontal = ('venues','permissions')

# Register your models here.
admin.site.register(Profile)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Activities, ActivityAdmin)
admin.site.register(HomeModuleNames, HomeModuleNamesAdmin)
admin.site.register(Client)
admin.site.register(Client_user_permissions, Client_user_permissions_admin)
