from .models import *

admin = User.objects.create_user(email = "tonyl7126@gmail.com", username = "tonyl7126@gmail.com", password = "test_password")
team = Team.objects.create(admin = admin, name = "team_name")
for x in range(7):
	team.users.add(User.objects.create(email = "user%d@gmail.com" % x, username = "user%d@gmail.com" % x))

