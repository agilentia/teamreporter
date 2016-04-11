var app = angular.module("teamreporterapp")
app.factory("userService", ["User", function(User){
	var users = [];
	var service = {
		init: function(team_id) {
			query = User.get({team_id: team_id}, function(data){
				users = data.users;
			});
			return query.$promise;
		},

		get: function(){
			return users;
		},

		save: function(team_id, user_info) {
			console.log(user_info)
			save = User.save({team_id: team_id}, user_info, function(data){
				console.log(data.user);
				users.push(data.user);
			});
			return save.$promise;
		},

		delete: function(team_id, user_id) {
			User.delete({team_id: team_id, id: user_id}, function(data){
				for (var i = 0; i < users.length; i++ ) {
					if (users[i].id == data.user.id){
						users.splice(i, 1);
					}
				}
			});
		},

		userModel: {users: users}

	}

	return service
}]);