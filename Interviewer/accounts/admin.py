from django.contrib import admin
from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display=('date', 'facial_expressions_keys', 'facial_expressions_values', 'audio_analysis_keys', 'audio_analysis_values', 'average_face_emotions', 'average_audio_emotions')

admin.site.register(Profile, ProfileAdmin)
# Register your models here.
