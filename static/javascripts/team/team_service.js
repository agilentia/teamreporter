var app = angular.module("teamreporterapp")
app.factory("teamService", ["$http", function($http){

	var service = {
		get: function(team) {
			return $http({
				method: 'GET',
				url: "/team/",
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				console.log(resp.data.teams);
				return {teams: resp.data.teams}
			}, function(error){
				return {error: error}
			});
		},

		save: function(team, user_email) {

		},
	}

	return service
}]);