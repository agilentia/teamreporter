var app = angular.module("teamreporterapp")
app.factory("teamService", ["Team", function(Team){
	var teams = [];
	var service = {
		init: function() {
			query = Team.get(function(data){
				console.log(data);
				teams = data.teams;
			}, function(response){
				// deal with exception
			});
			return query.$promise;
		},

		get: function(){
			return teams;
		},

		save: function(team_id, user_info) {
			console.log(user_info)
			save = Team.save({team_id: team_id}, user_info, function(data){
				teams.push(data.team);
			});
			return save.$promise;
		},

		delete: function(team_id) {
			User.delete({team_id: team_id}, function(data){
				for (var i = 0; i < teams.length; i++ ) {
					if (teams[i].id == data.team.id){
						teams.splice(i, 1);
					}
				}
			});
		},

		teamModel: {teams: teams}

	}

	return service
}]);