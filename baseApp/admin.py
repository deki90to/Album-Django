from django.contrib import admin
from django.contrib.auth.models import Group
from members.models import CustomUser
from . models import Season, Album, Comment, Year, Images


admin.site.unregister(Group)


# class UserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     fields = ['email']

# admin.site.unregister(CustomUser)

# admin.site.register(CustomUser)
# admin.site.register(UserAdmin)


admin.site.register(Season)
admin.site.register(Year)
admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Images)

