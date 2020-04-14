from django.db import models
# from tutorial.quickstart.common.models import GUIDModel

class User(models.Model):
	user_id = models.CharField(unique=True, max_length=36)
	display_name = models.CharField(max_length=64)
	points = models.IntegerField(default=0)
	rank = models.IntegerField(default=None)
	country = models.CharField(max_length=2, default="UNK")

	def __str__(self):
		# Defined for printing Users
		return f"{self.display_name} - {self.points} - {self.rank} - {self.country}"
