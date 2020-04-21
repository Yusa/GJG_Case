from django.db import models
import uuid
# from tutorial.quickstart.common.models import GUIDModel

class User(models.Model):
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	display_name = models.CharField(max_length=64)
	points = models.IntegerField(default=0)
	rank = models.IntegerField(default=None)
	country = models.CharField(max_length=2, default="UN")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		# Defined for printing Users
		return f"{self.user_id} - {self.display_name} - {self.points} - {self.rank} - {self.country}"



class ScoreSubmitHistory(models.Model):
	user_id = models.UUIDField()
	created_at = models.DateTimeField(auto_now_add=True)
	min_rank = models.IntegerField()
	max_rank = models.IntegerField()

	def __str__(self):
		# Defined for printing Users
		return f"By {self.user_id} at {self.created_at}. Affected Rank Interval: {self.min_rank} - {self.max_rank}"
