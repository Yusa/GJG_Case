from rest_framework import serializers
from .models import User

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


class LeaderboardSerializer(serializers.ModelSerializer):
	rank = serializers.IntegerField(required=True)
	points = serializers.IntegerField(required=True)
	display_name = serializers.CharField(required=True, allow_blank=False, max_length=64)
	country = serializers.CharField(required=True, max_length=5)

	# def create(self, validated_data):
	# 	"""
	# 	Create and return a new `User` instance, given the validated data.
	# 	"""
	# 	return User.objects.create(**validated_data)


	# def update(self, instance, validated_data):
	# 	"""
	# 	Update and return an existing `User` instance, given the validated data.
	# 	"""
	# 	instance.user_id = validated_data.get('user_id', instance.user_id)
	# 	instance.display_name = validated_data.get('display_name', instance.display_name)
	# 	instance.score = validated_data.get('score', instance.score)
	# 	instance.rank = validated_data.get('rank', instance.rank)
	# 	instance.save()
	# 	return instance

	class Meta:
		model = User
		fields = ('display_name', 'points', 'rank', 'country')



class UserProfileSerializer(serializers.ModelSerializer):
	user_id = serializers.CharField(required=True, allow_blank=False, max_length=36)
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