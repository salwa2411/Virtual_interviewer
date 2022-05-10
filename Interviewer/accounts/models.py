from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
	date = models.DateTimeField()
	facial_expressions_keys = models.CharField(max_length=50, default='')
	facial_expressions_values = models.CharField(max_length=50, default='')
	audio_analysis_keys = models.CharField(max_length=50, default='')
	audio_analysis_values = models.CharField(max_length=50, default='')
	average_face_emotions = models.CharField(max_length=50, default='')
	average_audio_emotions = models.CharField(max_length=50, default='')
	
	def date_now(self):
	    return self.time.strftime('%d/%m/%Y %H:%M:%S')