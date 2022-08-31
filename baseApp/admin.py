from django.contrib import admin
from . models import Season, Album, Comment, Year, Images


admin.site.register(Season)
admin.site.register(Year)
admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Images)