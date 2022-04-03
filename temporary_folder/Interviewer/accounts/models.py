from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
	date = models.DateField()
	facial_expressions = models.CharField(max_length=50)
	audio_analysis = models.CharField(max_length=50)
	accuracy = models.CharField(max_length=50)
