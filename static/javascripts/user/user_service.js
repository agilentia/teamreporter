var app = angular.module("teamreporterapp")
app.factory("userService", ["User", function(User){
	var users = [];
	var self = this;
	var service = {
		init: function(team_id) {
			self.team_id = team_id;
			query = User.get({team_id: team_id}, function(data){
				users = data.users;
			});
			return query.$promise;
		},

		get: function(){
			return users;
		},

		save: function(user_info) {
			save = User.save({team_id: self.team_id}, user_info, function(data){
				if ("user" in data) {
					users.push(data.user);
				}
				
			});
			return save.$promise;
		},

		delete: function(user_id) {
			User.delete({team_id: self.team_id, id: user_id}, function(data){
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