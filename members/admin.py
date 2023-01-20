from django.contrib import admin
from . models import CustomUser, Profile


admin.site.register(CustomUser)
admin.site.register(Profile)


# class ProfileInline(admin.StackedInline):
#     model = Profile

# class CustomUserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     fields = ['email']
#     inlines = [ProfileInline]