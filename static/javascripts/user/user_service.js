var app = angular.module("teamreporterapp")
app.factory("userService", ["$http", "$rootScope", function($http, $rootScope){

	var service = {
		get: function(team) {
			return $http({
				method: 'GET',
				url: "/team/" + team + "/users/", 
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				var user_obj = {users: resp.data.users};
				return user_obj
			}, function(error){
				return {error: error}
			});
		},

		save: function(team, user_info) {
			return $http({
				method: 'POST',
				url: "/team/" + team + "/users/",
				data: user_info,
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				var user_obj = {user: resp.data.user};
				$rootScope.$broadcast('user_added', user_obj)
				return user_obj

			}, function(error){
				return {error: error}
			});
		},

		delete: function(team, user_id) {

		}
	}

	return service
}]);