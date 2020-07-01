''' Admin module features added here.. '''
from django.contrib import admin
from .models        import Venue, Room, RoomType, Activities, HomeModuleNames
from .models        import Profile, Client, Client_user_permissions


class HomeModuleNamesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class ClientUserPermissionsAdmin(admin.ModelAdmin):
    ''' Admin module for Profile model '''
    filter_horizontal = ('venues', 'permissions')

# Register your models here.
admin.site.register(Profile)
admin.site.register(Venue)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Activities)
admin.site.register(HomeModuleNames, HomeModuleNamesAdmin)
admin.site.register(Client)
admin.site.register(Client_user_permissions, ClientUserPermissionsAdmin)
