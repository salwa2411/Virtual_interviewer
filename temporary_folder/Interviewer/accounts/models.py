from django.db import models

# Create your models here.
class Profile(models.Model):
	date = models.DateField()
	facial_expressions = models.CharField(max_length=50)
	audio_analysis = models.CharField(max_length=50)
	accuracy = models.CharField(max_length=50)
