from django.test import Client, TestCase
from django.core.urlresolvers import reverse
import unittest
from .models import Team, User
import json

class TestTeamAPI(TestCase):
	fixtures = ["teamreporter/fixtures/test_fixture1.json"]
	def setUp(self):
		self.client = Client()
		self.client.login(username = "tonyl7126@gmail.com", password= "test_password")

	def test_get_teams(self):
		response = self.client.get(reverse("team_view"))
		assert response.status_code == 200
		resp_data = json.loads(response.content.decode("utf-8"))
		assert "teams" in resp_data
		assert len(resp_data["teams"]) == 1
		assert "name" in resp_data["teams"][0]
		assert resp_data["teams"][0]["name"] == "team_name"

		#TODO: test unauthorized user

	def test_save_team(self):
		"""test saving a team"""

		#tests valid Team JSON
		team_info = {"name": "team1"}
		response = self.client.post(reverse("team_view"), content_type='application/json', data=json.dumps(team_info))
		assert response.status_code == 200

		#tests valid Team JSON with extra keys (should be cleaned)
		team_info = {"name": "team2", "b":"d"}
		response = self.client.post(reverse("team_view"), content_type='application/json', data=json.dumps(team_info))
		assert response.status_code == 200

		#tests invalid team JSON
		team_info = {"nam": "team2"}
		response = self.client.post(reverse("team_view"), content_type='application/json', data=json.dumps(team_info))
		assert response.status_code == 400

		#TODO: test unauthorized user

	def tearDown(self):
		pass


class TestUserAPI(TestCase):
	fixtures = ["teamreporter/fixtures/test_fixture1.json"]
	def setUp(self):
		self.client = Client()
		self.client.login(username = "tonyl7126@gmail.com", password= "test_password")

	def test_get_team_users(self):
		response = self.client.get(reverse("user_view", kwargs = {"team_id": 4}))