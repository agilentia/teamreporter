var app = angular.module("teamreporterapp")
app.factory("teamService", ["$http", "$rootScope", function($http, $rootScope){

	var service = {
		get: function(team) {
			return $http({
				method: 'GET',
				url: "/team/",
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				return {teams: resp.data.teams}
			}, function(error){
				return {error: error}
			});
		},

		save: function(team_info) {
			return $http({
				method: 'POST',
				url: "/team/",
				data: {name: team_info.name},
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				$rootScope.$broadcast('team_added', resp.data.team)
				return {team: resp.data.team}
			}, function(error){
				return {error: error}
			});
		},

		delete: function(team_id) {

		}
	}

	return service
}]);