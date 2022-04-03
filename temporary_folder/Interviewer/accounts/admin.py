from django.contrib import admin
from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display=('date', 'facial_expressions', 'audio_analysis', 'accuracy')

admin.site.register(Profile, ProfileAdmin)
# Register your models here.
