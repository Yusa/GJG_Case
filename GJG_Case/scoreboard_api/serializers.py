from rest_framework import serializers
from .models import User, ScoreSubmitHistory
from django.db import connection
import uuid
import GJG_Case.settings as settings
from django.utils import timezone

class LeaderboardSerializer(serializers.ModelSerializer):
	rank = serializers.IntegerField(required=True)
	points = serializers.IntegerField(required=True)
	display_name = serializers.CharField(required=True, allow_blank=False, max_length=64)
	country = serializers.CharField(required=True, allow_blank=False, max_length=2, min_length=2)
	# updated_at = serializers.DateTimeField()

	def create(self, validated_data):
		"""
		Create and return a new `User` instance, given the validated data.
		"""
		return User.objects.create(**validated_data)


	def update(self, instance, validated_data):
		"""
		Update and return an existing `User` instance, given the validated data.
		"""
		instance.user_id = validated_data.get('user_id', instance.user_id)
		instance.display_name = validated_data.get('display_name', instance.display_name)
		instance.score = validated_data.get('score', instance.score)
		instance.rank = validated_data.get('rank', instance.rank)
		# instance.updated_at = timezone.now()

		instance.save()
		return instance


	class Meta:
		model = User
		fields = ('display_name', 'points', 'rank', 'country')



class UserProfileSerializer(serializers.ModelSerializer):
	user_id = serializers.UUIDField(required=True, format="hex_verbose")
	display_name = serializers.CharField(required=True, allow_blank=False, max_length=64)
	points = serializers.IntegerField(required=True)
	rank = serializers.IntegerField(required=True)

	def create(self, validated_data):
		"""
		Create and return a new `User` instance, given the validated data.
		"""
		return User.objects.create(**validated_data)


	class Meta:
		model = User
		fields = ('display_name', 'points', 'rank', 'user_id')



class ScoreSubmitSerializer(serializers.ModelSerializer):
	user_id = serializers.UUIDField(required=True, format="hex_verbose")
	score_worth = serializers.IntegerField(required=True)
	timestamp = serializers.IntegerField(required=True)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `User` instance, given the validated data.
		"""
		instance.points += validated_data.get('score_worth', instance.points)

		# Raw SQL query is used to change every score in one query 
		# and avoid mass query for changing every users rank 
		# with connection.cursor() as cursor:
		# 	cursor.execute("""UPDATE scoreboard_api_user
		# 						SET rank = rank + 1
		# 						WHERE points < %s AND rank < %s""", 
		# 						[instance.points, instance.rank])
		#
		# With the above SQL approach, it takes 30seconds to update 600.000 records.
		# However The approach on the project is not updating all scores immediately.
		# Instead, scores of the affected users are updated when queried.

		rank_new = User.objects.filter(points__gte=instance.points).count() + 1

		historyData = {'user_id':instance.user_id, 'created_at':timezone.now(), 'max_rank':instance.rank, 'min_rank':rank_new}
		history_serializer = ScoreHistorySerializer(data=historyData)
		if history_serializer.is_valid():
			history_serializer.save()

		instance.rank = rank_new
		instance.save()

		return instance

	class Meta:
		model = User
		fields = ('user_id','score_worth', 'timestamp')



class BulkUserSerializer(serializers.ModelSerializer):
	user_id = serializers.UUIDField(required=True, format="hex_verbose")
	display_name = serializers.CharField(required=True, allow_blank=False, max_length=64)
	points = serializers.IntegerField(required=True)
	rank = serializers.IntegerField(required=True)
	country = serializers.CharField(required=True, allow_blank=False, max_length=2, min_length=2)

	def create(self, validated_data):
		"""
		Create and return a new `User` instance, given the validated data.
		"""
		return User.objects.create(**validated_data)


	class Meta:
		model = User
		fields = ('display_name', 'points', 'rank', 'country', 'user_id')



class ScoreHistorySerializer(serializers.ModelSerializer):
	user_id = serializers.UUIDField(required=True, format="hex_verbose")
	created_at = serializers.DateTimeField()
	min_rank = serializers.IntegerField()
	max_rank = serializers.IntegerField()


	def create(self, validated_data):
		"""
		Create and return a new `ScoreHistory` instance, given the validated data.
		"""
		return ScoreSubmitHistory.objects.create(**validated_data)


	class Meta:
		model = ScoreSubmitHistory
		fields = ('user_id', 'created_at', 'min_rank', 'max_rank')