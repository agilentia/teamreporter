var app = angular.module("teamreporterapp")
app.factory("teamService", ["Team", function(Team){
	var teams = [];
	var service = {
		init: function() {
			var query = Team.get(function(data){
				teams = data.teams;
			}, function(response){
				// deal with exception
			});
			return query.$promise;
		},

		get: function(){
			return teams;
		},

		save: function(team_info) {
			var save = Team.save(team_info, function(data){
				if ("team" in data)
					teams.push(data.team);
			});
			return save.$promise;
		},

		update: function(team_id, team_info) {
			var update = Team.update({id: team_id}, team_info, function(data){
				if ("team" in data) {
					for(var i = 0; i < teams.length; i++) {
						if (teams[i].id === data.team.id) {
							teams[i] = data.team;
						}
					}
				}
			});
			return update.$promise;
		},

		delete: function(team_id) {
			Team.delete({team_id: team_id}, function(data){
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