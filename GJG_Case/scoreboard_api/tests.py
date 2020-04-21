from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory
from GJG_Case.scoreboard_api.models import User
from GJG_Case.scoreboard_api.views import UserListNewView, LeaderboardView, ScoreView
import json

class UserCreateTestCase(TestCase):
	def setUp(self):
		User.objects.create(display_name="Ilyic", rank=3, points=1750, user_id="4fe63c05-11e1-4a2d-acff-85dbbc2c7abe" ,country="RU")
		User.objects.create(display_name="Mahir", rank=4, points=995, user_id="9c767715-3b9a-42c1-9510-976ae599e64b" ,country="TR")
		User.objects.create(display_name="Robespierre", rank=5, points=502, user_id="db59d4b2-8a7b-46c1-9397-10f2af995bc2" ,country="FR")


	def test_user_create_success(self):
		# Trying successful create
		factory = APIRequestFactory()
		user1 = {
					"display_name":"Karl",
					"rank":1,
					"points":1950,
					"user_id":"05050f82-b8b9-470c-a2d7-31311c18a679",
					"country":"DE"
				}
		request = factory.post('/user/create/', json.dumps(user1), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 201
		print("UserCreate Case 1 Successful")



	def test_user_create_fail1(self):
		# Trying to create user with existing user_id
		factory = APIRequestFactory()
		user2 = {
					"display_name":"Friedrich",
					"rank":2,
					"points":1930,
					"user_id":"4fe63c05-11e1-4a2d-acff-85dbbc2c7abe",
					"country":"DE"
				}
		request = factory.post('/user/create/', json.dumps(user2), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		assert response.data == {"error":"User already exists."}
		print("UserCreate Case 2 Successful")



	def test_user_create_fail2(self):
		# Trying to create user without parameter: country
		factory = APIRequestFactory()
		user3 = {
					"display_name":"Ilyic",
					"rank":3,
					"points":1750,
					"user_id":"4fe63c05-11e1-4a2d-acff-85dbbc2c7abe"
				}
		request = factory.post('/user/create/', json.dumps(user3), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 3 Successful")


	def test_user_create_fail3(self):
		# Trying to create user without parameter: user_id
		factory = APIRequestFactory()
		user4 = {
					"display_name":"Mahir",
					"rank":4,
					"points":995,
					"country":"TR"
				}
		request = factory.post('/user/create/', json.dumps(user4), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 4 Successful")


	def test_user_create_fail4(self):
		# Trying to create user without parameter: points
		factory = APIRequestFactory()
		user5 = {
					"display_name":"Robespierre",
					"rank":5,
					"user_id":"db59d4b2-8a7b-46c1-9397-10f2af995bc2",
					"country":"FR"
				}
		request = factory.post('/user/create/', json.dumps(user5), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 5 Successful")
		

	def test_user_create_fail5(self):
		# Trying to create user without parameter: rank
		factory = APIRequestFactory()
		user5 = {
					"display_name":"Robespierre",
					"points":995,
					"user_id":"db59d4b2-8a7b-46c1-9397-10f2af995bc2",
					"country":"FR"
				}
		request = factory.post('/user/create/', json.dumps(user5), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 6 Successful")


	def test_user_create_fail6(self):
		# Trying to create user without parameter: display_name
		factory = APIRequestFactory()
		user5 = {
					"rank":5,
					"points":995,
					"user_id":"db59d4b2-8a7b-46c1-9397-10f2af995bc2",
					"country":"FR"
				}
		request = factory.post('/user/create/', json.dumps(user5), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 7 Successful")


	def test_user_create_fail7(self):
		# Trying to create user with empty json
		factory = APIRequestFactory()
		user5 = {}
		request = factory.post('/user/create/', json.dumps(user5), content_type='application/json')
		view = UserListNewView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("UserCreate Case 8 Successful")





class UserProfileTestCase(TestCase):
	def setUp(self):
		User.objects.create(display_name="Ilyic", rank=3, points=1750, user_id="4fe63c05-11e1-4a2d-acff-85dbbc2c7abe" ,country="RU")
		User.objects.create(display_name="Mahir", rank=4, points=995, user_id="9c767715-3b9a-42c1-9510-976ae599e64b" ,country="TR")
		User.objects.create(display_name="Robespierre", rank=5, points=502, user_id="db59d4b2-8a7b-46c1-9397-10f2af995bc2" ,country="FR")


	def test_user_create_success(self):
		# Trying successful get profile operation
		factory = APIRequestFactory()
		user1 = {
					"display_name":"Ilyic",
					"rank":3,
					"points":1750,
					"user_id":"4fe63c05-11e1-4a2d-acff-85dbbc2c7abe"
				}
		request = factory.get(f'/user/profile/{user1["user_id"]}')
		view = UserListNewView.as_view()
		response = view(request, user1['user_id'])
		assert response.status_code == 200
		assert response.data == user1
		print("UserProfile Case 1 Successful")


	def test_user_create_fail1(self):
		# Trying to get a user profile with non-existing user_id
		factory = APIRequestFactory()
		user_id = "ffffffff-1111-4444-aaaa-aaaaaaaaaaaa"
		request = factory.get(f'/user/profile/{user_id}')
		view = UserListNewView.as_view()
		response = view(request, user_id)
		assert response.status_code == 400
		assert response.data == {"error": "User doesn't exist"}
		print("UserProfile Case 2 Successful")


	def test_user_create_fail2(self):
		# Trying to get user profile without giving user_id
		factory = APIRequestFactory()
		request = factory.get(f'/user/profile/')
		view = UserListNewView.as_view()
		response = view(request, "")
		assert response.status_code == 400
		assert response.data == {"error": "User ID is not given in the correct format."}
		print("UserProfile Case 3 Successful")





class LeaderboardTestCase(TestCase):
	def setUp(self):
		User.objects.create(display_name="Karl", rank=1, points=1950, user_id="05050f82-b8b9-470c-a2d7-31311c18a679" ,country="de")
		User.objects.create(display_name="Friedrich", rank=2, points=1930, user_id="63afa900-c978-43fa-8d6b-9f79aa9b0aee" ,country="de")		
		User.objects.create(display_name="Ilyic", rank=3, points=1750, user_id="4fe63c05-11e1-4a2d-acff-85dbbc2c7abe" ,country="ru")
		User.objects.create(display_name="Mahir", rank=4, points=995, user_id="9c767715-3b9a-42c1-9510-976ae599e64b" ,country="tr")
		User.objects.create(display_name="Robespierre", rank=5, points=502, user_id="db59d4b2-8a7b-46c1-9397-10f2af995bc2" ,country="fr")


	def test_leaderboard_all(self):
		# Trying to get all leaderboard
		factory = APIRequestFactory()
		request = factory.get(f'/leaderboard/')
		view = LeaderboardView.as_view()
		response = view(request)
		response.render()
		assert response.status_code == 200
		expected = {'count': 5, 'next': None, 'previous': None, 'results': [{'display_name': 'Karl', 'points': 1950, 'rank': 1, 'country': 'de'}, {'display_name': 'Friedrich', 'points': 1930, 'rank': 2, 'country': 'de'}, {'display_name': 'Ilyic', 'points': 1750, 'rank': 3, 'country': 'ru'}, {'display_name': 'Mahir', 'points': 995, 'rank': 4, 'country': 'tr'}, {'display_name': 'Robespierre', 'points': 502, 'rank': 5, 'country': 'fr'}]}
		assert json.loads(response.content) == expected
		print("Leaderboard Case 1 Successful")


	def test_leaderboard_country_success(self):
		# Trying to get leaderboard of a correctly given country code
		factory = APIRequestFactory()
		request = factory.get(f'/leaderboard/de/')
		view = LeaderboardView.as_view()
		response = view(request, "de")
		response.render()
		assert response.status_code == 200
		assert json.loads(response.content) == {'count': 2, 'next': None, 'previous': None, 'results': [{'display_name': 'Karl', 'points': 1950, 'rank': 1, 'country': 'de'}, {'display_name': 'Friedrich', 'points': 1930, 'rank': 2, 'country': 'de'}]}
		print("Leaderboard Case 2 Successful")


	def test_leaderboard_country_fail1(self):
		# Trying to get leaderboard of a correctly given country code
		factory = APIRequestFactory()
		request = factory.get(f'/leaderboard/ff/')
		view = LeaderboardView.as_view()
		response = view(request, "ff")
		assert response.status_code == 200
		assert response.data == {"result":"No user record exists for the given country code."}
		print("Leaderboard Case 3 Successful")


	def test_leaderboard_country_fail2(self):
		# Trying to get leaderboard of a falsely given country code
		factory = APIRequestFactory()
		request = factory.get(f'/leaderboard/asdf/')
		view = LeaderboardView.as_view()
		response = view(request, "asdf")
		assert response.status_code == 400
		assert response.data == {"error":"Country code is not valid."}
		print("Leaderboard Case 4 Successful")

	def test_leaderboard_country_fail3(self):
		# Trying to get leaderboard of a falsely given country code
		factory = APIRequestFactory()
		request = factory.get(f'/leaderboard/t5/')
		view = LeaderboardView.as_view()
		response = view(request, "t5")
		assert response.status_code == 400
		assert response.data == {"error":"Country code is not valid."}
		print("Leaderboard Case 5 Successful")


class ScoreSubmitTestCase(TestCase):
	def setUp(self):
		User.objects.create(display_name="Karl", rank=1, points=1950, user_id="05050f82-b8b9-470c-a2d7-31311c18a679" ,country="de")
		User.objects.create(display_name="Friedrich", rank=2, points=1930, user_id="63afa900-c978-43fa-8d6b-9f79aa9b0aee" ,country="de")		
		User.objects.create(display_name="Ilyic", rank=3, points=1750, user_id="4fe63c05-11e1-4a2d-acff-85dbbc2c7abe" ,country="ru")
		User.objects.create(display_name="Mahir", rank=4, points=995, user_id="9c767715-3b9a-42c1-9510-976ae599e64b" ,country="tr")
		User.objects.create(display_name="Robespierre", rank=5, points=502, user_id="db59d4b2-8a7b-46c1-9397-10f2af995bc2" ,country="fr")


	def testScoreChange(self):
		# Trying successful update
		factory = APIRequestFactory()
		score_change = {
					"score_worth":4000,
					"user_id":"9c767715-3b9a-42c1-9510-976ae599e64b",
					"timestamp":1231412351
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 200
		assert response.data == {"result":"1"}

		user1 = {
					"display_name":"Mahir",
					"rank":1,
					"points":4995,
					"user_id":"9c767715-3b9a-42c1-9510-976ae599e64b"
				}
		request = factory.get(f'/user/profile/{user1["user_id"]}')
		view = UserListNewView.as_view()
		response = view(request, user1['user_id'])
		assert response.status_code == 200
		assert response.data == user1

		user2 = {
					"display_name":"Karl",
					"rank":2,
					"points":1950,
					"user_id":"05050f82-b8b9-470c-a2d7-31311c18a679"
				}

		request = factory.get(f'/user/profile/{user2["user_id"]}')
		view = UserListNewView.as_view()
		response = view(request, user2['user_id'])
		assert response.status_code == 200
		assert response.data == user2		

		print("ScoreSubmit Case 1 Successful")


	def testScoreChange_fail1(self):
		# Trying failed update due to non-existing user_id 
		factory = APIRequestFactory()
		score_change = {
					"score_worth":100,
					"user_id":"ffffffff-ffff-ffff-ffff-ffffffffffff",
					"timestamp":1231412351
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		assert response.data == {"error":"User with given user_id does not exists."}
		print("ScoreSubmit Case 2 Successful")


	def testScoreChange_fail2(self):
		# Trying failed update due to json without score_worth 
		factory = APIRequestFactory()
		score_change = {
					"user_id":"05050f82-b8b9-470c-a2d7-31311c18a679",
					"timestamp":1231412351
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("ScoreSubmit Case 3 Successful")

	def testScoreChange_fail3(self):
		# Trying failed update due to json without user_id 
		factory = APIRequestFactory()
		score_change = {
					"score_worth":100,
					"timestamp":1231412351
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("ScoreSubmit Case 4 Successful")

	def testScoreChange_fail4(self):
		# Trying failed update due to json without timestamp 
		factory = APIRequestFactory()
		score_change = {
					"score_worth":100,
					"user_id":"05050f82-b8b9-470c-a2d7-31311c18a679"
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("ScoreSubmit Case 5 Successful")

	def testScoreChange_fail5(self):
		# Trying failed update due to empty json 
		factory = APIRequestFactory()
		score_change = {
				}
		request = factory.post('/score/submit/', json.dumps(score_change), content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("ScoreSubmit Case 6 Successful")

	def testScoreChange_fail6(self):
		# Trying failed update due to no json sent
		factory = APIRequestFactory()
		request = factory.post('/score/submit/', content_type='application/json')
		view = ScoreView.as_view()
		response = view(request)
		assert response.status_code == 400
		print("ScoreSubmit Case 7 Successful")