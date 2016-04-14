from .tasks import send_survey, generate_survey, send_summary, issue_summaries, issue_surveys
from unittest.mock import Mock
from django.test import Client, TestCase

class TestTasks(TestCase):
	def setUp(self):
		pass